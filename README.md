pyziptax
========

Python API for Zip-Tax.com

Installation
------------
`pip install pyziptax`

Usage Example
-------------
```
import decimal
import pyziptax
client = pyziptax.ZipTaxClient(ZIPTAX_KEY)
rate = client.get_rate('10000', 'new_york_city', 'NY')
# rate == decimal.Decimal('8.875')
```

ZipTaxClient Parameters
-----------------------
 - `ZIPTAX_KEY` - API key you received when you registered on Zip-Tax.com
 - `zip_code` - The only required parameter
 - `city` - Optional
 - `state` - Optional
 - `multiple_rates` - If `True`, returns a dictionary of city names to tax rates;
                      If `False`, returns just the tax rate, but raises a
                      ZipTaxFailure if multiple rates were returned.
