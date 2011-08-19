#!/usr/bin/python


""" Reader for CSV files.
"""


from __future__ import absolute_import
from csv import DictReader
import functools

from pysheets.exceptions import InvalidFileError
from pysheets.readers import SheetReader


class CSVReader(SheetReader):
    """ CSV file reader.
    """

    name = u'Comma separated values'
    short_name = u'CSV'
    file_extensions = [u'csv',]
    mime_type = 'text/csv'

    def read(
            self, sheet, file, create_columns=True,
            dialect='excel', delimiter=';', quotechar='\"'):
        """ Reads data from given file into sheet.

        Arguments ``dialect``, ``delimiter`` and ``quotechar`` are
        passed to CSV reader. For documentation look
        `here <http://docs.python.org/library/csv.html#csv.DictReader>`_
        """

        reader = DictReader(
                file, dialect=dialect, delimiter=delimiter,
                quotechar=quotechar)
        if not reader.fieldnames:
            raise InvalidFileError(
                    u'Trying to read empty or badly formated sheet.')

        if create_columns:
            captions_set = set(sheet.captions)
            for caption in reader.fieldnames:
                caption = caption.decode('utf-8')
                if caption not in captions_set:
                    sheet.add_column(caption)

        for row in reader:
            sheet.append_dict(dict([
                (key.decode('utf-8'), value.decode('utf-8'))
                for key, value in row.items()]))

    @functools.wraps(read)
    def __call__(self, sheet, file, *args, **kwargs):
        """ Wrapper function, which ensures that file is file like
        object.
        """

        if isinstance(file, unicode):
            with open(file, 'rb') as fp:
                self.read(sheet, fp, *args, **kwargs)
        else:
            self.read(sheet, file, *args, **kwargs)
