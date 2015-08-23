# Settings
api_key = None
url = 'http://api.zip-tax.com/request/v20'

# Imports
from .ziptax import ZipTaxClient, get_rate
from .exceptions import *
