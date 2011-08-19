#!/usr/bin/python


import unittest
import os
from cStringIO import StringIO

from pysheets.exceptions import IntegrityError
from pysheets.readers.csv import CSVReader
from pysheets.sheet import Sheet


class CSVReaderTest(unittest.TestCase):
    """ Tests for :py:class:`pysheets.readers.csv.CSVReader`.
    """

    def assertSheet(self, sheet):
        self.assertEqual(len(sheet), 2)
        self.assertEqual(
                sheet.captions, [u'Name', u'E-Mail', u'Phone numbers'])
        self.assertEqual(
                [list(row) for row in sheet],
                [
                    [
                        u'Foo Bar',
                        u'foo@example.com',
                        u'+37060000000;+37061111111'],
                    [
                        u'Fooer Barer',
                        u'bar@example.com',
                        u'+37062222222']])

    def test_01(self):

        data = StringIO('''\
"Name";"E-Mail";"Phone numbers"
"Foo Bar";"foo@example.com";"+37060000000;+37061111111"
"Fooer Barer";"bar@example.com";"+37062222222"\
''')
        reader = CSVReader()
        sheet = Sheet()
        self.assertEqual(len(sheet), 0)
        self.assertEqual(sheet.captions, [])

        reader(sheet, data)
        self.assertSheet(sheet)

    def test_02(self):

        data = StringIO('''\
`Name`&`E-Mail`&`Phone numbers`
`Foo Bar`&`foo@example.com`&`+37060000000;+37061111111`
`Fooer Barer`&`bar@example.com`&`+37062222222`\
''')
        reader = CSVReader()
        sheet = Sheet()
        self.assertEqual(len(sheet), 0)
        self.assertEqual(sheet.captions, [])

        reader(sheet, data, delimiter='&', quotechar='`')
        self.assertSheet(sheet)

    def test_03(self):

        data = StringIO('''\
"Name";"E-Mail";"Phone numbers"
"Foo Bar";"foo@example.com";"+37060000000;+37061111111"
"Fooer Barer";"bar@example.com";"+37062222222"\
''')
        reader = CSVReader()
        sheet = Sheet()

        self.assertRaises(
                IntegrityError, reader, sheet, data, create_columns=False)


    def test_04(self):

        file = os.path.join(os.path.dirname(__file__), 'files', 'sheet.csv')

        reader = CSVReader()
        sheet = Sheet()
        self.assertEqual(len(sheet), 0)
        self.assertEqual(sheet.captions, [])
        reader(sheet, file.decode('utf-8'))
        self.assertEqual(len(sheet), 2)
        self.assertEqual(
                sheet.captions, [u'Name', u'E-Mail', u'Phone numbers'])

    def test_05(self):

        file = os.path.join(os.path.dirname(__file__), 'files', 'sheet.csv')

        reader = CSVReader()
        sheet = Sheet()
        sheet.add_column(u'Name')
        self.assertEqual(len(sheet), 0)
        self.assertEqual(sheet.captions, [u'Name'])
        reader(sheet, file.decode('utf-8'), create_columns=False)
        self.assertEqual(len(sheet), 2)
        self.assertEqual(
                sheet.captions, [u'Name'])
        self.assertEqual(
                [list(row) for row in sheet],
                [[u'Foo Bar'], [u'Fooer Barer']])
