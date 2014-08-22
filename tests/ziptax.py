import decimal
import unittest

from mock import patch

from pyziptax.ziptax import ZipTaxClient

class ZipTaxTest(unittest.TestCase):
    @patch('pyziptax.ziptax.requests')
    def test_get_rate(self, mock_requests):
        mock_requests.get().json.return_value = {'rCode': 100, 'results': [{'taxSales': 0.08}]}
        client = ZipTaxClient('asdf')
        tax_rate = client.get_rate('12345')
        self.assertEqual(mock_requests.get.call_args[0][0], ZipTaxClient.url)
        self.assertEqual(mock_requests.get.call_args[1]['params']['key'], 'asdf')
        self.assertEqual(mock_requests.get.call_args[1]['params']['postalcode'], '12345')
        self.assertEqual(tax_rate, decimal.Decimal('8.000'))

class ZipTaxMakeRequestTest(unittest.TestCase):
    def setUp(self):
        self.client = ZipTaxClient('asdf')

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

class ZipTaxProcessResponseTest(unittest.TestCase):
    def test_process_response(self):
        pass
