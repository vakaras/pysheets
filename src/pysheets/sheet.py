#!/usr/bin/python


"""

:py:class:`Sheet` is implemented as a list of :py:class:`rows <Row>`.

:py:class:`Row` is a list of values in the same order, in which
:py:class:`Sheet` :py:attr:`captions <Sheet.captions>` are listed.
:py:class:`Row` fields access by column caption is emulated.

:py:class:`Column` is just a view object.


"""


class Sheet(object):
    """ Class representing simple sheet.
    """

    def __init__(
            self, file=None, reader_name=None, reader_class=None,
            rows=None, reader_args=None):
        """ Creates sheet.

        #.  If ``rows`` is not ``None``, then sheet is created from
            data provided at ``rows``.
        #.  If ``file`` is not ``None``, then data is read from it.

        If ``reader_name`` and ``reader_class`` is None, then it is
        expected that file is an unicode string with path to a file to
        read information from and which reader to use is tried to guess
        by file name extension.

        :param file: File from which to read data.
        :type file: unicode or file like object.
        :param reader_name: Name of the reader to use.
        :type reader_name: None or unicode.
        :param reader_class: Class of the reader to use.
        :type reader_class: None or class.

        """

        self.captions = []
        self.captions_index = {}        # Caption to field index mapping.
        self.rows = []

        if rows is not None:
            try:
                self.add_columns(rows[0].keys())
            except IndexError:
                pass
            else:
                for row in rows:
                    self.append(row)
        elif file or reader_name or reader_class:
            self.read(file, reader_name, reader_class, reader_args)

    def add_column(self, caption):
        """ Appends column to the right side of sheet.
        """

        self.captions_index[caption] = len(self.captions)
        self.captions.append(caption)

    def add_columns(self, captions):
        """ Appends columns to the right side of sheet.
        """

        for caption in captions:
            self.add_column(caption)
