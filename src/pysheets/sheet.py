#!/usr/bin/python


"""

:py:class:`Sheet` is implemented as a list of :py:class:`rows <Row>`.

:py:class:`Row` is a list of values in the same order, in which
:py:class:`Sheet` :py:attr:`captions <Sheet.captions>` are listed.
:py:class:`Row` fields access by column caption is emulated.

:py:class:`Column` is just a view object.

>>> from pysheets.sheet import Sheet, Row, Column

"""


from pysheets.exceptions import IntegrityError
import pysheets.readers
from pysheets.readers import SheetReader


class Row(object):
    """ Class representing sheet row.
    """

    def __init__(self, sheet, fields):

        self.sheet = sheet
        self.fields = fields

    def __getitem__(self, caption):
        return self.fields[self.sheet.captions_index[caption]]

    def __setitem__(self, caption, value):
        self.fields[self.sheet.captions_index[caption]] = value

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

    def __getitem__(self, index):
        return self.sheet.rows[index].fields[self.index]

    def __setitem__(self, index, value):
        self.sheet.rows[index].fields[self.index] = value

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
            self, file=None, reader_name=None, reader=None,
            rows=None, captions=None, reader_args=None):
        """ Creates sheet.

        #.  If ``rows`` is not ``None``, then sheet is created from
            data provided at ``rows``.
        #.  If ``file`` is not ``None``, then data is read from it.

        If ``reader_name`` and ``reader`` is None, then it is expected
        that file is an unicode string with path to a file to read
        information from and which reader to use is tried to guess by
        file name extension.

        :param file: File from which to read data.
        :type file: unicode or file like object.
        :param reader_name: Name of the reader to use.
        :type reader_name: None or unicode.
        :param reader: Callable to use for reading file.
        :type reader: None or callable.

        """

        self.captions = []
        self.captions_index = {}        # Caption to field index mapping.
        self.rows = []
        self.insert_validators = []
        self.delete_validators = []
        self.replace_validators = []

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
        elif file:
            self.read(file, True, reader_name, reader, reader_args)

    def __len__(self):
        return len(self.rows)

    def __iter__(self):
        return iter(self.rows)

    def __getitem__(self, index):
        return self.rows[index]

    def __setitem__(self, index, row):

        replaced_row = self.rows[index]
        for validator in self.replace_validators:
            row = validator(self, row, replaced_row)
        self.rows[index] = Row(
                self, [row[caption] for caption in self.captions])

    def __delitem__(self, index):

        row = self.rows[index]
        for validator in self.delete_validators:
            validator(self, row)
        del self.rows[index]

    def read(
            self, file, create_columns=False, reader_name=None,
            reader=None, reader_args=None):
        """ Reads data from file into sheet.

        :param file: File from which to read data.
        :type file: unicode or file like object.
        :param reader_name: Name of the reader to use.
        :type reader_name: None or unicode.
        :param reader: Callable to use for reading file.
        :type reader: None or callable.
        """

        if reader is None:
            if reader_name:
                reader = SheetReader.plugins[reader_name]()
            else:
                reader = SheetReader.plugins.get_by_file(file)()
        reader(self, file, create_columns, **(reader_args or {}))

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

        if not self.captions:
            raise IntegrityError(
                    u'Adding data to sheet with zero columns.')

        for validator in self.insert_validators:
            row = validator(self, row)

        self.rows.append(
                Row(self, [row[caption] for caption in self.captions]))

    def append_iterable(self, row):
        """ Appends row to the end of sheet.

        :type row: iterable
        """

        if not self.captions:
            raise IntegrityError(
                    u'Adding data to sheet with zero columns.')

        fields = list(row)
        if len(fields) != len(self.captions):
            raise ValueError((
                u'Columns number mismatch. Expected {0}. Is {1}.'
                ).format(len(self.captions), len(fields)))
        elif self.insert_validators:
            # There are some validators. Converting to dict.
            self.append_dict(dict([
                (caption, value)
                for caption, value in zip(self.captions, row)]))
        else:
            # There is no validators. Just appending row.
            self.rows.append(Row(self, fields))

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
            return
        except KeyError:
            pass
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
        iterable of lists, which have just one element, a column is
        returned.

        """

        if len(captions) == 1:
            return Column(self, self.captions_index[captions[0]])
        else:
            return ([row[caption] for caption in captions]
                    for row in self.rows)

    def remove(self, caption):
        """ Removes column from sheet.
        """

        if len(self.captions) == 1:
            # Deleting last column, so just delete all rows.
            self.rows = []
            self.captions = []
            self.captions_index = {}
        else:
            index = self.captions_index[caption]
            del self.captions[index]

            for row in self.rows:
                del row.fields[index]

            # Regenerate caption index.
            self.captions_index = dict([
                (caption, i) for i, caption in enumerate(self.captions)])

    def filter(self, func):
        """ Returns iterator through rows, for which ``func`` returns
        :py:class:`True`.
        """

        for row in self.rows:
            if func(row):
                yield row

    def sort(self, columns=None, cmp=None, key=None, **kwargs):
        """ Sorts rows of the sheet.

        :param columns: iterable of column, by which to compare, captions

        .. note::
            If ``cmp`` or ``key`` is provided, then argument
            ``columns`` is ignored.

        """

        if cmp or key:
            self.rows.sort(cmp=cmp, key=key, **kwargs)
        elif columns is None:
            self.rows.sort(key=lambda x: x.fields)
        else:
            def key(row):
                """ Returns sort key for the given row.
                """
                return [row.fields[self.captions_index[caption]]
                        for caption in columns]
            self.rows.sort(key=key, **kwargs)

    def add_insert_validator(self, validator):
        """ Adds validator to insert validators queue.
        """

        self.insert_validators.append(validator)

    def add_delete_validator(self, validator):
        """ Adds validator to delete validators queue.
        """

        self.delete_validators.append(validator)

    def add_replace_validator(self, validator):
        """ Adds validator to replace validators queue
        """

        self.replace_validators.append(validator)

    def add_validator(self, validator, *types):
        """ Adds validator to validators lists mentioned in ``types``.

        """

        for validator_type in types:
            if validator_type == 'insert':
                self.add_insert_validator(validator)
            elif validator_type == 'delete':
                self.add_delete_validator(validator)
            elif validator_type == 'replace':
                self.add_replace_validator(validator)
            else:
                raise ValueError(
                        u'Unknown validator type: \"{0}\".'.format(
                            validator_type))


# Init built-in readers. (Silently.)
for reader_module in pysheets.readers.__all__:
    try:
        __import__('pysheets.readers', fromlist=[reader_module], level=0)
    except ImportError:
        pass
