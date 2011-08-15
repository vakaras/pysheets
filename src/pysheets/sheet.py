#!/usr/bin/python


"""

:py:class:`Sheet` is implemented as a list of :py:class:`rows <Row>`.

:py:class:`Row` is a list of values in the same order, in which
:py:class:`Sheet` :py:attr:`captions <Sheet.captions>` are listed.
:py:class:`Row` fields access by column caption is emulated.

:py:class:`Column` is just a view object.

>>> from pysheets.sheet import Sheet, Row, Column

"""


class Row(object):
    """ Class representing sheet row.
    """

    def __init__(self, sheet, index, fields):

        self.sheet = sheet
        self.index = index
        self.fields = fields

    def __getitem__(self, caption):
        return self.fields[self.sheet.captions_index[caption]]

    def __iter__(self):
        return iter(self.fields)

    def append(self, field):
        """ Appends new field to the row.
        """

        self.fields.append(field)

    def keys(self):
        """ Returns :py:attr:`Sheet.captions`.
        """

        return self.sheet.captions


class Column(object):
    """ Class represinting single sheet column.

    .. note::
        Column is just a view. It doesn't contain any data.

        >>> sheet = Sheet(rows=[{u'a': 1, u'b': 2}])
        >>> col1, col2 = sheet.columns
        >>> col1.caption
        u'a'
        >>> col2.caption
        u'b'
        >>> sheet.captions[0] = u'c'    # This is just for example.
        ...                             # You shouldn't modify column
        ...                             # captions in this way.
        ...                             # FIXME: Create normal example.
        >>> col1.caption
        u'c'

    """

    def __init__(self, sheet, index):

        self.sheet = sheet
        self.index = index

    def __iter__(self):
        for row in self.sheet.rows:
            yield row.fields[self.index]

    @property
    def caption(self):
        """ Returns caption of the column.
        """

        return self.sheet.captions[self.index]



class Sheet(object):
    """ Class representing simple sheet.

    .. py:attribute:: captions

        List of columns captions. This attribute should be used
        as read only:

        >>> sheet = Sheet(rows=[{u'a': 1, u'b': 2}])
        >>> print u', '.join(sheet.captions)
        a, b

    """

    def __init__(
            self, file=None, reader_name=None, reader_class=None,
            rows=None, captions=None, reader_args=None):
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

        if captions:
            self.add_columns(captions)

        if rows is not None:
            rows = list(rows)
            if captions:
                # Rows can be both -- dicts and iterables.
                for row in rows:
                    self.append(row)
            else:
                # All rows have to be dicts.
                try:
                    self.add_columns(rows[0].keys())
                except IndexError:
                    pass
                else:
                    for row in rows:
                        self.append_dict(row)
        elif file or reader_name or reader_class:
            self.read(file, reader_name, reader_class, reader_args)

    def __len__(self):
        return len(self.rows)

    def __iter__(self):
        return iter(self.rows)

    def __getitem__(self, index):
        return self.rows[index]

    def add_column(self, caption, values=()):
        """ Appends column to the right side of sheet.
        """

        if len(self.rows) != len(values):
            raise ValueError((
                u'Rows number mismatch. Expected {0}. Is {1}.'
                ).format(len(self.rows), len(values)))

        self.captions_index[caption] = len(self.captions)
        self.captions.append(caption)

        for row, value in zip(self.rows, values):
            row.append(value)

    def add_columns(self, captions):
        """ Appends columns to the right side of sheet.
        """

        for caption in captions:
            self.add_column(caption)

    def append_dict(self, row):
        """ Appends row to the end of sheet.

        :type row: dict-like
        """

        fields = []
        for caption in self.captions:
            fields.append(row[caption])

        self.rows.append(Row(self, len(self.rows), fields))

    def append_iterable(self, row):
        """ Appends row to the end of sheet.

        :type row: iterable
        """

        fields = list(row)
        if len(fields) != len(self.captions):
            raise ValueError((
                u'Columns number mismatch. Expected {0}. Is {1}.'
                ).format(len(self.captions), len(fields)))
        else:
            self.rows.append(Row(self, len(self.rows), fields))

    def append(self, row):
        """ Appends row to the end of sheet.

        ``row`` is expected to be an iterable with fields in the same
        order as :py:attr:`Sheet.captions` (the amount of elements
        must match) or dict-like object, which has all captions in keys.

        Firstly it is tried to treat row as a dict and if it raises
        :py:class:`TypeError` then it is tried to iterate through
        it.

        """

        try:
            row[self.captions[0]]
        except TypeError:
            self.append_iterable(row)
        else:
            self.append_dict(row)

    @property
    def columns(self):
        """ Returns iterator through columns in the same order as
        :py:attr:`captions`.

        """

        for i, caption in enumerate(self.captions):
            yield Column(self, i)

    def get(self, *captions):
        """ Returns iterable through subset of columns defined by
        captions.

        If just one caption is provided than instead of returning
        iterable of lists, which have just one element, a iterable of
        elements is returned.

        """

        if len(captions) == 1:
            caption = captions[0]
            for row in self.rows:
                yield row[caption]
        else:
            for row in self.rows:
                yield [row[caption] for caption in captions]

    def filter(self, func):
        """ Returns iterator through rows, for which ``func`` returns
        :py:class:`True`.
        """

        for row in self.rows:
            if func(row):
                yield row
