pyziptax
========

|Latest Version| |License|

|Codeship Status for albertyw/pyziptax| |Dependency Status| |Code
Climate|

Python API for Zip-Tax.com

Installation
------------

``pip install pyziptax``

Usage Example
-------------

.. code:: python

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

ZipTaxClient Parameters
-----------------------

-  ``ZIPTAX_KEY`` - API key you received when you registered on
   Zip-Tax.com
-  ``zip_code`` - The only required parameter
-  ``city`` - Optional
-  ``state`` - Optional
-  ``multiple_rates`` - If ``True``, returns a dictionary of city names
   to tax rates; If ``False``, returns just the tax rate, but raises a
   ZipTaxFailure if multiple rates were returned.

Development
-----------

Pull requests welcome!

.. code:: shell

    # Set up repository for development
    pip install tox
    python setup.py install

    # Run tests
    tox

To update PyPI:

.. code:: shell

    pip install twine
    python setup.py sdist bdist_wheel
    twine upload dist/*

.. |Latest Version| image:: https://img.shields.io/pypi/v/pyziptax.svg
   :target: https://pypi.python.org/pypi/pyziptax/
.. |License| image:: https://img.shields.io/pypi/l/pyziptax.svg
   :target: https://pypi.python.org/pypi/pyziptax/
.. |Codeship Status for albertyw/pyziptax| image:: https://codeship.com/projects/ac619bb0-acba-0132-14f9-4e5346bb67f3/status?branch=master
   :target: https://codeship.com/projects/68576
.. |Dependency Status| image:: https://gemnasium.com/albertyw/pyziptax.svg
   :target: https://gemnasium.com/albertyw/pyziptax
.. |Code Climate| image:: https://codeclimate.com/github/albertyw/pyziptax/badges/gpa.svg
   :target: https://codeclimate.com/github/albertyw/pyziptax
