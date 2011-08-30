#!/usr/bin/python


import unittest
import os
import datetime
import tempfile
from cStringIO import StringIO

from pysheets.exceptions import IntegrityError, InvalidFileError
from pysheets.writers.csv import CSVWriter
from pysheets.sheet import Sheet


class CSVWriterTest(unittest.TestCase):
    """ Tests for :py:class:`pysheets.writers.csv.CSVWriter`.
    """

    def setUp(self):

        self.sheet = Sheet(
                captions=[u'Number', u'Square', u'Cube'],
                rows=[(i, i * i, i * i * i) for i in range(5)])
        self.file = StringIO()

    def test_01(self):

        writer = CSVWriter()
        writer(self.sheet, self.file)
        self.assertEqual(
                self.file.getvalue(),
                """\
"Number";"Square";"Cube"
"0";"0";"0"
"1";"1";"1"
"2";"4";"8"
"3";"9";"27"
"4";"16";"64"
"""
                )

    def test_02(self):

        writer = CSVWriter(delimiter='&', quotechar='`')
        writer(self.sheet, self.file)
        self.assertEqual(
                self.file.getvalue(),
                """\
`Number`&`Square`&`Cube`
`0`&`0`&`0`
`1`&`1`&`1`
`2`&`4`&`8`
`3`&`9`&`27`
`4`&`16`&`64`
"""
                )

    def test_03(self):

        self.sheet.add_column('Today', [datetime.date(2011, 8, 30)] * 5)
        self.sheet.add_column(
                'Now', [datetime.datetime(2011, 8, 30, 12, 58, 53)] * 5)
        writer = CSVWriter()
        writer(self.sheet, self.file)
        self.assertEqual(
                self.file.getvalue(),
                """\
"Number";"Square";"Cube";"Today";"Now"
"0";"0";"0";"2011-08-30";"2011-08-30 12:58:53"
"1";"1";"1";"2011-08-30";"2011-08-30 12:58:53"
"2";"4";"8";"2011-08-30";"2011-08-30 12:58:53"
"3";"9";"27";"2011-08-30";"2011-08-30 12:58:53"
"4";"16";"64";"2011-08-30";"2011-08-30 12:58:53"
"""
                )

    def test_04(self):

        writer = CSVWriter()
        file_descriptor, file_path = tempfile.mkstemp(suffix='.csv')
        file_path = file_path.decode('utf-8')
        writer(self.sheet, file_path)

        with open(file_path, 'rb') as fp:
            contents = fp.read()

        self.assertEqual(
                contents,
                """\
"Number";"Square";"Cube"
"0";"0";"0"
"1";"1";"1"
"2";"4";"8"
"3";"9";"27"
"4";"16";"64"
"""
                )
