"""
This module contains the code to make requests to Ziptax to fetch tax rates
for a given address
"""

from decimal import Decimal

import requests


class ZipTaxFailure(Exception):
    pass


class ZipTaxClient(object):
    url = 'http://api.zip-tax.com/request/v20'

    def __init__(self, key):
        self.api_key = key

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
        if resp['rCode'] != 100:
            # invalid something here
            raise ZipTaxFailure(
                'invalid request: return code is %s' % resp['rCode'])

        results = resp['results']
        if len(results) == 0:
            raise ZipTaxFailure('No results found for params %s' % data)
        if len(results) > 1 and not multiple_rates:
            # It's fine if all the taxes are the same
            rates = [result['taxSales'] for result in results]
            if len(set(rates)) != 1:
                raise ZipTaxFailure('Multiple results found for params %s' % data)

        if multiple_rates:
            rates = {}
            for result in results:
                rate = result['taxSales']
                rate = (Decimal(rate) * 100).quantize(Decimal('0.001'))
                rates[result['geoCity']] = float(rate)
            return rates
        else:
            rate = results[0]['taxSales']
            rate = (Decimal(rate) * 100).quantize(Decimal('0.001'))
            return rate
