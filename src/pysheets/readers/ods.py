#!/usr/bin/python


"""

Readers for ODF Spreadsheet files.

>>> from odf.opendocument import load
>>> from odf.table import Table, TableRow, TableCell
>>> doc = load('src/pysheets/test/files/sheet.ods')
>>>
>>> # Reading.
>>> table, = doc.getElementsByType(Table)
>>> print table.getAttribute('name')
>>> for row in table.getElementsByType(TableRow):
...     for cell in row.childNodes:
...         print cell.childNodes[0].childNodes[0].data,
...     print
>>>
>>> # Writing.
>>> table2 = Table(name=u'bla')
>>> doc.spreadsheet.addElement(table2)
>>> doc.write('src/pysheets/test/files/sheet2.ods')

"""


from odf.opendocument import load
from odf.table import Table, TableRow

from pysheets.exceptions import InvalidFileError
from pysheets.readers import SheetReader, SpreadSheetReader


def row_values_generator(row, default_value):
    """ Generates infinitive sequence of row cells values.
    """
    for cell in row.childNodes:
        for i in range(int(cell.attributes.get(
            (u'urn:oasis:names:tc:opendocument:xmlns:table:1.0',
                u'number-columns-repeated'), 1))):
            try:
                yield cell.firstChild.firstChild.data
            except AttributeError:
                yield default_value


def generate_row_dict(row, captions, default_value):
    """ Generates dict for :meth:`Sheet.append_dict` method.
    """

    return dict([
        (caption, value)
        for caption, value in zip(
            captions, row_values_generator(row, default_value))
        ])


def insert_to_sheet(iterator, sheet, captions, default_value):
    """ Inserts data from ods row iterator into sheet.
    """

    for row in iterator:
        sheet.append_dict(
                generate_row_dict(row, captions, default_value))


class ODFSheetReader(SheetReader):
    """ ODS file reader. (Expects, that there is only one sheet in
    document.)
    """

    name = u'Open Document Format, Sheet'
    short_name = u'ODSS'                # ODS Sheet
    file_extensions = [u'ods']
    mime_type = 'application/vnd.oasis.opendocument.spreadsheet'

    def __call__(
            self, sheet, filename, create_columns=True, sheet_name=None,
            default_value=None):
        """ Reads data from given file into sheet.

        :param sheet_name: Name of the sheet to read from document.
        :type sheet_name: unicode.
        :param default_value: Value of nonexistent cells.

        .. note::
            If ``sheet_name`` is None and document has more than one
            sheet, then :py:exec:`ValueError` is raised.
        """

        doc = load(filename)
        tables = doc.getElementsByType(Table)
        if sheet_name:
            for table in tables:
                if table.getAttribute('name') == sheet_name:
                    break
            else:
                raise ValueError(
                        u'No sheet with name "{0}".'.format(sheet_name))
        else:
            table, = tables

        iterator = iter(table.getElementsByType(TableRow))
        try:
            captions = [
                    unicode(caption_node.firstChild.firstChild.data)
                    for caption_node in iterator.next().childNodes]
        except (StopIteration, AttributeError):
            raise InvalidFileError(u'Trying to read empty sheet.')

        if create_columns:
            captions_set = set(sheet.captions)
            for caption in captions:
                if caption not in captions_set:
                    sheet.add_column(caption)

        insert_to_sheet(iterator, sheet, captions, default_value)


class ODFSpreadSheetReader(SpreadSheetReader):
    """ ODS file reader.
    """

    name = u'Open Document Format'
    short_name = u'ODS'
    file_extensions = [u'ods']
    mime_type = 'application/vnd.oasis.opendocument.spreadsheet'

    def __call__(
            self, spreadsheet, filename, default_value=None,
            read_sheets=None, ignore_sheets=()):
        """ Reads data from given file into sheet.

        :param sheet_name: Name of the sheet to read from document.
        :type sheet_name: unicode.
        :param default_value: Value of nonexistent cells.
        :param read_sheets: Iterable of sheets to read in. ``None``
            means all.
        :param ignore_sheets: Iterable of sheets to not read in.

        """

        doc = load(filename)

        for table in doc.getElementsByType(Table):

            name = unicode(table.getAttribute('name'))
            if read_sheets is not None:
                if name not in read_sheets:
                    continue
            if name in ignore_sheets:
                continue

            iterator = iter(table.getElementsByType(TableRow))
            try:
                captions = [
                        unicode(caption_node.firstChild.firstChild.data)
                        for caption_node in iterator.next().childNodes]
            except (StopIteration, AttributeError):
                raise InvalidFileError(u'Trying to read empty sheet.')

            sheet = spreadsheet.create_sheet(name, captions=captions)

            insert_to_sheet(iterator, sheet, captions, default_value)
