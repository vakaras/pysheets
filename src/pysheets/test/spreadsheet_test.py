#!/usr/bin/python


import unittest
import os
from cStringIO import StringIO

from pysheets.exceptions import IntegrityError
from pysheets.sheet import Sheet
from pysheets.spreadsheet import SpreadSheet
from validators import (
        ValidationError,
        UniqueIntegerValidator,
        unique_integer_validator_creator, validate_nothing)


class SheetTest(unittest.TestCase):
    """ Tests for :py:class:`pysheets.sheet.Sheet`, when it is assigned
    to :py:class:`pysheets.sheet.SpreadSheet`.

    """

    def test_01(self):
        ss = SpreadSheet()

        self.assertEqual(ss.names, [])
        self.assertEqual(len(ss), 0)

        sheet1 = ss.create_sheet(u'sheet1')
        self.assertEqual(ss.names, [u'sheet1'])
        self.assertEqual(len(ss), 1)
        self.assertEqual(list(ss), [sheet1])
        self.assertIs(sheet1.spreadsheet, ss)
        self.assertEqual(sheet1.name, u'sheet1')
        self.assertIs(ss[u'sheet1'], sheet1)

        del ss[u'sheet1']
        self.assertIs(sheet1.name, None)
        self.assertIs(sheet1.spreadsheet, None)

    def test_02(self):

        ss = SpreadSheet()

        sheet1 = ss.create_sheet(u'sheet1')

        self.assertEqual(sheet1.insert_validators, [])
        self.assertEqual(sheet1.delete_validators, [])
        self.assertEqual(sheet1.replace_validators, [])

        ss.add_sheet_validator_creator(unique_integer_validator_creator)
        ss.add_sheet_validator(
                validate_nothing, 'insert', 'delete', 'replace')

        sheet2 = ss.create_sheet(u'sheet2')

        v1, v2 = sheet1.insert_validators
        self.assertIs(v2, validate_nothing)
        self.assertEqual(
                unicode(v1)[:91],
                u'<bound method UniqueIntegerValidator.insert of '
                u'<validators.UniqueIntegerValidator object at')

        v1, v2 = sheet1.delete_validators
        self.assertIs(v2, validate_nothing)
        self.assertEqual(
                unicode(v1)[:91],
                u'<bound method UniqueIntegerValidator.delete of '
                u'<validators.UniqueIntegerValidator object at')

        v1, v2 = sheet1.replace_validators
        self.assertIs(v2, validate_nothing)
        self.assertEqual(
                unicode(v1)[:92],
                u'<bound method UniqueIntegerValidator.replace of '
                u'<validators.UniqueIntegerValidator object at')

        v1, v2 = sheet2.insert_validators
        self.assertIs(v2, validate_nothing)
        self.assertEqual(
                unicode(v1)[:91],
                u'<bound method UniqueIntegerValidator.insert of '
                u'<validators.UniqueIntegerValidator object at')

        v1, v2 = sheet2.delete_validators
        self.assertIs(v2, validate_nothing)
        self.assertEqual(
                unicode(v1)[:91],
                u'<bound method UniqueIntegerValidator.delete of '
                u'<validators.UniqueIntegerValidator object at')

        v1, v2 = sheet2.replace_validators
        self.assertIs(v2, validate_nothing)
        self.assertEqual(
                unicode(v1)[:92],
                u'<bound method UniqueIntegerValidator.replace of '
                u'<validators.UniqueIntegerValidator object at')

        sheet1.add_column(u'ID')
        sheet1.append([1])
        sheet1.append([2])
        self.assertRaises(ValidationError, sheet1.append, [2])

        sheet2.add_column(u'ID')
        sheet2.append([2])

        sheet1[1] = {u'ID': 3}
        sheet1.append([2])
        del sheet1[1]

        self.assertEqual([row[u'ID'] for row in sheet1], [1, 2])
        self.assertEqual([row[u'ID'] for row in sheet2], [2])
