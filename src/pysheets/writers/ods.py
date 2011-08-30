#!/usr/bin/python


"""

Writer for ODF Spreadsheet files.

"""


import datetime

from odf.opendocument import OpenDocumentSpreadsheet
from odf.table import Table, TableRow, TableCell
from odf.text import P


from pysheets.writers import SpreadSheetWriter


class ODFSpreadSheetWriter(SpreadSheetWriter):
    """ ODS file reader.
    """

    name = u'Open Document Format'
    short_name = u'ODS'
    file_extensions = [u'ods']
    mime_type = 'application/vnd.oasis.opendocument.spreadsheet'

    def write_captions(self, sheet, table):
        """ Writes sheet's caption row to table.
        """

        row = TableRow()
        for caption in sheet.captions:
            cell = TableCell()
            cell.addElement(P(text=caption))
            row.addElement(cell)
        table.addElement(row)

    def write_row(self, sheet_row, table):
        """ Appends ``sheet_row`` data into table.
        """

        row = TableRow()
        for field in sheet_row:
            if isinstance(field, datetime.datetime):
                field = unicode(field.strftime('%Y-%m-%d %H:%M:%S'))
            elif isinstance(field, datetime.date):
                field = unicode(field.strftime('%Y-%m-%d'))
            elif not isinstance(field, unicode):
                field = unicode(field)
            cell = TableCell()
            cell.addElement(P(text=field))
            row.addElement(cell)

        table.addElement(row)

    def write_sheet(self, sheet, table):
        """ Writes sheet data into table.
        """

        self.write_captions(sheet, table)
        for row in sheet:
            self.write_row(row, table)

    def __call__(self, spreadsheet, file):
        """ Writes all data from spreadsheet into file.
        """

        doc = OpenDocumentSpreadsheet()

        for sheet in spreadsheet:
            table = Table(name=sheet.name)
            self.write_sheet(sheet, table)
            doc.spreadsheet.addElement(table)

        doc.write(file)
