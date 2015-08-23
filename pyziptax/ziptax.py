"""
This module contains the code to make requests to Ziptax to fetch tax rates
for a given address
"""

from decimal import Decimal

import requests

from pyziptax import exceptions

def get_rate(zipcode, city=None, state=None, multiple_rates=False):
    client = ZipTaxClient()
    return client.get_rate(zipcode, city, state, multiple_rates)

class ZipTaxClient(object):
    def __init__(self):
        from pyziptax import api_key, url
        self.url = url
        self.api_key = api_key
        if not self.api_key:
            raise exceptions.ZipTaxInvalidKey("No Zip-Tax.com key was given")

    def get_rate(self, zipcode, city=None, state=None, multiple_rates=False):
        """
        Finds sales tax for given info.
        Returns Decimal of the tax rate, e.g. 8.750.
        """
        data = self.make_request_data(zipcode, city, state)

        r = requests.get(self.url, params=data)
        resp = r.json()

        return self.process_response(resp, multiple_rates)

    def make_request_data(self, zipcode, city, state):
        """ Make the request params given location data """
        data = {'key': self.api_key,
                'postalcode': str(zipcode),
                'city': city,
                'state': state
        }
        data = ZipTaxClient._clean_request_data(data)
        return data

    @staticmethod
    def _clean_request_data(data):
        """ Remove empty values, and clean data """
        # Ziptax doesn't like 4 digit zip code extensions, strip them
        data['postalcode'] = data['postalcode'][:5]
        if not data['city']:
            del data['city']
        if not data['state']:
            del data['state']
        return data

    def process_response(self, resp, multiple_rates):
        """ Get the tax rate from the ZipTax response """
        self._check_for_exceptions(resp, multiple_rates)

        rates = {}
        for result in resp['results']:
            rate = ZipTaxClient._cast_tax_rate(result['taxSales'])
            rates[result['geoCity']] = rate
        if not multiple_rates:
            return rates[list(rates.keys())[0]]
        return rates

    def _check_for_exceptions(self, resp, multiple_rates):
        """ Check if there are exceptions that should be raised """
        if resp['rCode'] != 100:
            raise exceptions.get_exception_for_code(resp['rCode'])(resp)

        results = resp['results']
        if len(results) == 0:
            raise exceptions.ZipTaxNoResults('No results found')
        if len(results) > 1 and not multiple_rates:
            # It's fine if all the taxes are the same
            rates = [result['taxSales'] for result in results]
            if len(set(rates)) != 1:
                raise exceptions.ZipTaxMultipleResults('Multiple results found but requested only one')

    @staticmethod
    def _cast_tax_rate(raw_rate):
        """ Converts the tax rate from ZipTax into a decimal """
        return (Decimal(raw_rate) * 100).quantize(Decimal('0.001'))
