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
        make_request_data(zipcode, city, state)

        r = requests.get(self.url, params=data)
        resp = r.json()

        return process_response(resp, multiple_rates)

    def make_request_data(zipcode, city, state):
        """ Make the request params given location data """
        # Ziptax doesn't like 4 digit zip code extensions, strip them
        zipcode = str(zipcode)
        if len(zipcode) > 5:
            zipcode = zipcode[:5]

        data = {'key': self.api_key, 'postalcode': zipcode}
        if city is not None:
            data['city'] = city
        if state is not None:
            data['state'] = state
        return data

    def process_response(resp, multiple_rates):
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
