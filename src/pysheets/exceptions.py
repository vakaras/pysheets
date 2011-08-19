#!/usr/bin/python


"""

All non standard Python exceptions, which could be raised by pysheets.

"""


class PySheetException(Exception):
    """ Base class for all exceptions.
    """


class IntegrityError(PySheetException):
    """ Raised when integrity validation fails.
    """


class InvalidFileError(PySheetException):
    """ Raised when trying to read invalid file.
    """
