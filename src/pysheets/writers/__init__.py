#!/usr/bin/python


""" Plugin points for writers.
"""


from pysheets.plugins import MountPoint


class SheetWriter(object):
    """ Base class for any sheet writer.

    Plugin manager will look for these **class** attributes:

    +   ``name`` -- unicode string, the full name of writer (this will
        be used, when displaying messages to users);
    +   ``short_name`` -- unique (between writers) unicode string (it
        is used as writer identifier);
    +   ``file_extensions`` -- tuple of unicode strings (used for file
        type  guessing; without dot, for example: ``'ods'``);
    +   ``mime_type`` -- byte string;

    Writer have to be a callable, which gets arguments:

    +   ``sheet`` -- sheet, which data to output.
    +   ``file`` -- unicode string with path to file, or file like object.
    +   ``kwargs`` -- other options passed to :py:meth:`Sheet.write`.

    """

    __metaclass__ = MountPoint


class SpreadSheetWriter(object):
    """ Base class for any spreadsheet writer.

    Plugin manager will look for these **class** attributes:

    +   ``name`` -- unicode string, the full name of writer (this will
        be used, when displaying messages to users);
    +   ``short_name`` -- unique (between writers) unicode string (it
        is used as writer identifier);
    +   ``file_extensions`` -- tuple of unicode strings (used for file
        type  guessing; without dot, for example: ``'ods'``);
    +   ``mime_type`` -- byte string;

    Writer have to be a callable, which gets arguments:

    +   ``spreadsheet`` -- spreadsheet, which data to output.
    +   ``file`` -- unicode string with path to file, or file like object.
    +   ``kwargs`` -- other options passed to :py:meth:`Sheet.write`.

    """

    __metaclass__ = MountPoint
