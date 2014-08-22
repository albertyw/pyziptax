"""
This module contains all the exceptions that ZipTaxClient can throw
See http://docs.zip-tax.com/en/latest/api_response.html#response-codes
"""

class ZipTaxFailure(Exception):
    pass

class ZipTaxInvalidKey(ZipTaxFailure):
    pass

class ZipTaxInvalidFormat(ZipTaxFailure):
    pass

class ZipTaxInvalidData(ZipTaxFailure):
    pass

class ZipTaxInvalidState(ZipTaxInvalidData):
    pass

class ZipTaxInvalidCity(ZipTaxInvalidData):
    pass

class ZipTaxInvalidPostalCode(ZipTaxInvalidData):
    pass

class ZipTaxNoResults(ZipTaxFailure):
    pass

class ZipTaxMultipleResults(ZipTaxFailure):
    pass

def get_exception_for_code(code):
    exceptions = {
        101: ZipTaxInvalidKey,
        102: ZipTaxInvalidState,
        103: ZipTaxInvalidCity,
        104: ZipTaxInvalidPostalCode,
        105: ZipTaxInvalidFormat,
    }
    return exceptions.get(code, ZipTaxFailure)