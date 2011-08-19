#!/usr/bin/python


""" Plugin point for readers.
"""


from pysheets.plugins import MountPoint


class SheetReader(object):
    """ Base class for any sheet reader.

    Plugin manager will look for these **class** attributes:

    +   ``name`` -- unicode string, the full name of reader (this will
        be used, when displaying messages to users);
    +   ``short_name`` -- unique (between readers) unicode string (it
        is used as reader identifier);
    +   ``file_extensions`` -- tuple of unicode strings (used for file
        type  guessing; without dot, for example: ``'ods'``);
    +   ``mime_type`` -- byte string;

    Reader have to be a callable, which gets arguments:

    +   ``sheet`` -- sheet to which data have to added.
    +   ``file`` -- unicode string with path to file, or file like object.
    +   ``create_columns`` -- if True, then reader should create columns
        from file.
    +   ``kwargs`` -- other options passed to :py:meth:`Sheet.read`.

    """

    __metaclass__ = MountPoint


__all__ = ['csv', 'ods']
