#!/usr/bin/python


""" Writer for CSV files.
"""


from __future__ import absolute_import
import cStringIO
import csv
import functools
import datetime

from pysheets.writers import SheetWriter


class CSVWriter(SheetWriter):
    """ CSV file writer.
    """

    name = u'Comma separated values'
    short_name = u'CSV'
    file_extensions = [u'csv',]
    mime_type = 'text/csv'

    def __init__(
            self, dialect='excel', delimiter=';', quotechar='\"',
            lineterminator='\n', quoting=csv.QUOTE_ALL, encoding='utf-8'):
        super(CSVWriter, self).__init__()

        self.dialect = dialect
        self.delimiter = delimiter
        self.quotechar = quotechar
        self.lineterminator = lineterminator
        self.quoting = quoting
        self.encoding = encoding

    def write_row(self, row, writer):
        """ Converts each field into byte string, and passes to
        ``writer.writerow``.
        """

        encoded_row = []
        for field in row:
            if isinstance(field, datetime.datetime):
                field = field.strftime('%Y-%m-%d %H:%M:%S')
            elif isinstance(field, datetime.date):
                field = field.strftime('%Y-%m-%d')
            elif not isinstance(field, str):
                field = unicode(field).encode('utf-8')
            encoded_row.append(field)
        writer.writerow(encoded_row)

    def write(self, sheet, file):
        """ Writes data from sheet into file.
        """

        buffer = cStringIO.StringIO()
        writer = self.create_writer(buffer)

        write = lambda row: self.write_row(row, writer)

        write(sheet.captions)
        for row in sheet:
            write(row)
        file.write(buffer.getvalue().decode('utf-8').encode(self.encoding))

    def create_writer(self, file):
        """ Constructs CSV writer.
        """

        return csv.writer(
                file, dialect=self.dialect, delimiter=self.delimiter,
                quotechar=self.quotechar,
                lineterminator=self.lineterminator,
                quoting=self.quoting,
                )

    @functools.wraps(write)
    def __call__(self, sheet, file):
        """ Wrapper function, which ensures that ``file`` is file like
        object.
        """

        if isinstance(file, unicode):
            with open(file, 'wb') as fp:
                self.write(sheet, fp)
        else:
            self.write(sheet, file)
