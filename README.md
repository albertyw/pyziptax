pyziptax
========

[ ![Codeship Status for albertyw/pyziptax](https://codeship.com/projects/ac619bb0-acba-0132-14f9-4e5346bb67f3/status?branch=master)](https://codeship.com/projects/68576)

Python API for Zip-Tax.com

Installation
------------
`pip install pyziptax`

Usage Example
-------------
```python
import pyziptax

# Single Tax Rate
pyziptax.api_key = ZIPTAX_KEY
rate = pyziptax.get_rate('10001', 'New York', 'NY')
# import decimal
# rate == decimal.Decimal('8.875')

# Multiple Tax Rates
pyziptax.api_key = ZIPTAX_KEY
rate = pyziptax.get_rate('94304', multiple_rates=True)
# rate == {u'LOCKHEED': Decimal('8.250'), u'PALO ALTO': Decimal('8.750')}
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

Development
-----------
Pull requests welcome!

```shell
# Set up repository for development
python setup.py develop

# Run tests
python setup.py test
```
