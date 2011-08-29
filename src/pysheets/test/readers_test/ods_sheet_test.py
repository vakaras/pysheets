#!/usr/bin/python


import unittest
import os

from pysheets.exceptions import IntegrityError, InvalidFileError
from pysheets.readers.ods import ODFSheetReader, ODFSpreadSheetReader
from pysheets.sheet import Sheet
from pysheets.spreadsheet import SpreadSheet


class ODFSheetReaderTest01(unittest.TestCase):
    """ Tests for :py:class:`pysheets.readers.ods.ODFSheetReader`.

    Testing reading ODF file, which has only one table.
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
    def setUp(self):
        self.file = os.path.join(
                os.path.dirname(__file__), 'files', 'sheet.ods'
                ).decode('utf-8')
        self.reader = ODFSheetReader()
        self.sheet = Sheet()
        self.assertEqual(len(self.sheet), 0)
        self.assertEqual(self.sheet.captions, [])

    def tearDown(self):
        self.file = None
        self.reader = None
        self.sheet = None

    def test_01(self):

        self.reader(self.sheet, self.file)
        self.assertSheet(self.sheet)

    def test_02(self):

        self.reader(self.sheet, self.file, sheet_name=u'Sheet1')
        self.assertSheet(self.sheet)

    def test_03(self):

        self.assertRaises(
                ValueError, self.reader, self.sheet, self.file,
                sheet_name=u'Sheet2')

    def test_04(self):

        self.assertRaises(
                IntegrityError, self.reader, self.sheet, self.file,
                create_columns=False)

    def test_05(self):

        self.sheet.add_column(u'Name')

        self.reader(self.sheet, self.file, create_columns=False)
        self.assertEqual(
                [list(row) for row in self.sheet],
                [[u'Foo Bar'], [u'Fooer Barer']])


class ODFSheetReaderTest02(unittest.TestCase):
    """ Tests for :py:class:`pysheets.readers.ods.ODFSheetReader`.
    """

    def setUp(self):
        self.file = os.path.join(
                os.path.dirname(__file__), 'files', 'spreadsheet.ods'
                ).decode('utf-8')
        self.reader = ODFSheetReader()
        self.sheet = Sheet()
        self.assertEqual(len(self.sheet), 0)
        self.assertEqual(self.sheet.captions, [])

    def tearDown(self):
        self.file = None
        self.reader = None
        self.sheet = None

    def test_01(self):
        """ Should raise exception, because document have several sheets.
        """

        self.assertRaises(ValueError, self.reader, self.sheet, self.file)

    def test_02(self):

        self.reader(self.sheet, self.file, sheet_name=u'List')
        self.assertEqual(
                self.sheet.captions, [u'Name', u'E-Mail', u'Phone numbers'])
        self.assertEqual(
                [list(row) for row in self.sheet],
                [[
                    u'Foo Bar', u'foo@example.com',
                    u'+37060000000;+37061111111'],
                    [u'Fooer Barer', u'bar@example.com', u'+37062222222']])

    def test_03(self):

        self.reader(self.sheet, self.file, sheet_name=u'Formulas')
        self.assertEqual(
                self.sheet.captions,
                [u'Value', u'Factorial', u'Square', u'Cube'])
        self.assertEqual(
                [list(row) for row in self.sheet],
                [
                    [u'0', u'1', u'0', u'0'],
                    [u'1', u'1', u'1', u'1'],
                    [u'2', u'2', u'4', u'8'],
                    [u'3', u'6', u'9', u'27'],
                    [u'4', u'24', u'16', u'64'],
                    [u'5', u'120', u'25', u'125'],
                    [u'6', u'720', u'36', u'216'],
                    [u'7', u'5040', u'49', u'343'],
                    [u'8', u'40320', u'64', u'512'],
                    [u'9', u'362880', u'81', u'729'],
                    [u'10', u'3628800', u'100', u'1000']])


    def test_04(self):

        self.reader(self.sheet, self.file, sheet_name=u'Participants')
        self.assertEqual(
                self.sheet.captions,
                [
                    u'Participants', u'Event1', u'Event2',
                    u'Event3', u'Event4'])
        self.assertEqual(
                [list(row) for row in self.sheet],
                [
                    [u'Foo Bar1', u'1', None, None, u'1', ],
                    [u'Foo Bar2', None, None, None, None, ],
                    [u'Foo Bar3', None, u'1', None, None, ],
                    [u'Foo Bar4', None, None, None, u'1', ],
                    [u'Foo Bar5', u'1', None, None, None, ],
                    [u'Foo Bar6', None, None, u'1', None, ],
                    [u'Foo Bar7', u'1', None, None, None, ],
                    [u'Foo Bar8', None, None, u'1', None, ],
                    [u'Foo Bar9', None, u'1', None, None, ], ])

    def test_05(self):

        self.assertRaises(
                InvalidFileError, self.reader, self.sheet, self.file,
                sheet_name=u'Empty')


class ODFSpreadSheetReaderTest(unittest.TestCase):
    """ Tests for :py:class:`pysheets.readers.ods.ODFSpreadSheetReader`.
    """

    def setUp(self):
        self.file = os.path.join(
                os.path.dirname(__file__), 'files', 'spreadsheet.ods'
                ).decode('utf-8')
        self.reader = ODFSpreadSheetReader()
        self.ss = SpreadSheet()
        self.assertEqual(len(self.ss), 0)
        self.assertEqual(self.ss.names, [])

    def tearDown(self):
        self.file = None
        self.reader = None
        self.sheet = None

    def test_01(self):
        self.assertRaises(InvalidFileError, self.reader, self.ss, self.file)

    def test_02(self):
        self.reader(self.ss, self.file, ignore_sheets=[u'Empty'])
        self.assertEqual(len(self.ss), 3)
        self.assertEqual(
                self.ss.names, [u'List', u'Formulas', u'Participants'])
        sheet = self.ss[u'Participants']
        self.assertEqual(
                sheet.captions,
                [
                    u'Participants', u'Event1', u'Event2',
                    u'Event3', u'Event4'])
        self.assertEqual(
                [list(row) for row in sheet],
                [
                    [u'Foo Bar1', u'1', None, None, u'1', ],
                    [u'Foo Bar2', None, None, None, None, ],
                    [u'Foo Bar3', None, u'1', None, None, ],
                    [u'Foo Bar4', None, None, None, u'1', ],
                    [u'Foo Bar5', u'1', None, None, None, ],
                    [u'Foo Bar6', None, None, u'1', None, ],
                    [u'Foo Bar7', u'1', None, None, None, ],
                    [u'Foo Bar8', None, None, u'1', None, ],
                    [u'Foo Bar9', None, u'1', None, None, ], ])

    def test_03(self):
        self.reader(self.ss, self.file,
                read_sheets=[u'Participants', u'Empty', u'List'],
                ignore_sheets=[u'Empty'])
        self.assertEqual(len(self.ss), 2)
        self.assertEqual(
                self.ss.names, [u'List', u'Participants'])
