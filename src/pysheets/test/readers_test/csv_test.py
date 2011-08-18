#!/usr/bin/python


import unittest
import tempfile
from cStringIO import StringIO

from pysheets.exceptions import IntegrityError
from pysheets.readers.csv import CSVReader
from pysheets.sheet import Sheet


class CSVReaderTest(unittest.TestCase):
    """ Tests for :py:class:`pysheets.plugins.PluginManager`.
    """

    def assertSheet(self, sheet):
        self.assertEqual(len(sheet), 2)
        self.assertEqual(
                sheet.captions, [u'E-Mail', u'Name', u'Phone numbers'])
        self.assertEqual(
                [list(row) for row in sheet],
                [
                    [
                        u'foo@example.com',
                        u'Foo Bar',
                        u'+37060000000;+37061111111'],
                    [
                        u'bar@example.com',
                        u'Fooer Barer',
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

        data = ('''\
"Name";"E-Mail";"Phone numbers"
"Foo Bar";"foo@example.com";"+37060000000;+37061111111"
"Fooer Barer";"bar@example.com";"+37062222222"\
''')
        t, file = tempfile.mkstemp(suffix='.csv')
        with open(file, 'wb') as fp:
            fp.write(data)

        reader = CSVReader()
        sheet = Sheet()
        self.assertEqual(len(sheet), 0)
        self.assertEqual(sheet.captions, [])
        reader(sheet, file.decode('utf-8'))
        self.assertEqual(len(sheet), 2)
        self.assertEqual(
                sheet.captions, [u'E-Mail', u'Name', u'Phone numbers'])
