import decimal
import unittest

from mock import patch, MagicMock

from pyziptax import ZipTaxClient, exceptions


class ZipTaxTestBase(unittest.TestCase):
    def setUp(self):
        self.correctData = {
            'rCode': 100,
            'results': [{
                'taxSales': 0.08,
                'geoCity': 'San Francisco',
            }],
        }
        self.client = ZipTaxClient('asdf')


class ZipTaxTest(ZipTaxTestBase):
    @patch('pyziptax.ziptax.requests')
    def test_get_rate(self, mock_requests):
        """ Can get the tax rate """
        mock_requests.get().json.return_value = self.correctData
        tax_rate = self.client.get_rate('12345')
        self.assertEqual(mock_requests.get.call_args[0][0], ZipTaxClient.url)
        self.assertEqual(mock_requests.get.call_args[1]['params']['key'], 'asdf')
        self.assertEqual(mock_requests.get.call_args[1]['params']['postalcode'], '12345')
        self.assertEqual(tax_rate, decimal.Decimal('8.000'))


class ZipTaxMakeRequestTest(ZipTaxTestBase):
    def test_make_request_data(self):
        """ Will make a proper params dictionary from given values """
        data = self.client.make_request_data('12345', 'mock_city', 'mock_state')
        self.assertEqual(data['key'], 'asdf')
        self.assertEqual(data['postalcode'], '12345')
        self.assertEqual(data['city'], 'mock_city')
        self.assertEqual(data['state'], 'mock_state')

    def test_incomplete_data(self):
        """ Will not include data that is not given """
        data = self.client.make_request_data('12345', None, None)
        self.assertFalse('city' in data)
        self.assertFalse('state' in data)

    def test_zipcode_max_length(self):
        """ Will strip 4 digit zip code extensions if given """
        data = self.client.make_request_data('12345-6789', None, None)
        self.assertEqual(data['postalcode'], '12345')


class ZipTaxCheckForExceptions(ZipTaxTestBase):
    def test_invalid_key(self):
        """ Raises an error if a non-100 response code is returned """
        self.correctData['rCode'] = 101
        with self.assertRaises(exceptions.ZipTaxInvalidKey):
            self.client._check_for_exceptions(self.correctData, False)

    def test_no_results(self):
        """ Raises an error if there are no results returned """
        self.correctData['results'] = []
        with self.assertRaises(exceptions.ZipTaxNoResults):
            self.client._check_for_exceptions(self.correctData, False)

    def test_multiple_rates(self):
        """ Raises an error if multiple results are returned but requested one """
        self.correctData['results'].append({'taxSales': 0.07})
        with self.assertRaises(exceptions.ZipTaxMultipleResults):
            self.client._check_for_exceptions(self.correctData, False)

    def test_multiple_duplicate_rates(self):
        """ Won't raise an error if multiple results with the same tax rate are returned """
        self.correctData['results'].append({'taxSales': 0.08})
        self.client._check_for_exceptions(self.correctData, False)

    def test_multiple_requested_rates(self):
        """ Won't raise an error if multiple rates are requested """
        self.correctData['results'].append({'taxSales': 0.07})
        self.client._check_for_exceptions(self.correctData, True)


class ZipTaxProcessResponse(ZipTaxTestBase):
    def test_process_response(self):
        """ Will return a tax rate when a single result is requested """
        rate = self.client.process_response(self.correctData, False)
        self.assertEqual(rate, decimal.Decimal('8.000'))

    def test_process_response_multiple(self):
        """ Will return a dict of tax rates when multiple results are requested """
        rate = self.client.process_response(self.correctData, True)
        self.assertEqual(rate, {'San Francisco': decimal.Decimal('8.000')})

    def test_process_response_multiple_results(self):
        """ Will return multiple results """
        self.correctData['results'].append({'taxSales': 0.07, 'geoCity': 'Boston'})
        rate = self.client.process_response(self.correctData, True)
        self.assertEqual(rate['San Francisco'], decimal.Decimal('8.000'))
        self.assertEqual(rate['Boston'], decimal.Decimal('7.000'))

    def test_validates(self):
        """ Will check for exceptions before processing response """
        mock_check = MagicMock()
        self.client._check_for_exceptions = mock_check
        self.client.process_response(self.correctData, False)
        self.assertEqual(mock_check.call_args[0][0], self.correctData)
        self.assertEqual(mock_check.call_args[0][1], False)


class ZipTaxCastTaxRate(ZipTaxTestBase):
    def test_tax_casting(self):
        """ Casts tax rates correctly """
        rate = self.client._cast_tax_rate(0.08875)
        self.assertEqual(rate, decimal.Decimal('8.8750'))
