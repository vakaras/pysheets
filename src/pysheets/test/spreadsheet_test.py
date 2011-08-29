#!/usr/bin/python


import unittest
import os
from cStringIO import StringIO

from pysheets.exceptions import IntegrityError
from pysheets.sheet import Sheet
from pysheets.spreadsheet import SpreadSheet
from validators import (
        ValidationError,
        UniqueIntegerValidator, SheetOrder,
        integer_gid, UniqueIntegerValidator2,
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


class SpreadSheetTest(unittest.TestCase):
    """ Tests for :py:class:`pysheets.sheet.SpreadSheet`.
    """

    def test_01(self):

        ss = SpreadSheet(names=[u'sheet1', u'sheet2'])
        self.assertEqual(len(ss), 2)

        self.assertRaises(IntegrityError, ss.create_sheet, u'sheet1')

        validator = SheetOrder()
        ss.add_validator(validator.add, 'add_sheet')
        ss.add_validator(validator.remove, 'remove_sheet')

        self.assertRaises(ValueError, ss.create_sheet, u'sheet3')
        self.assertEqual(len(ss), 2)
        ss.create_sheet(u'  1    ')
        ss.create_sheet(u'  2    ')
        self.assertRaises(ValidationError, ss.create_sheet, u'      1    ')

        self.assertRaises(ValueError, ss.__delitem__, u'sheet1')
        self.assertRaises(ValidationError, ss.__delitem__, u'1')
        del ss[u'2']

    def test_02(self):

        ss = SpreadSheet(
                names=[u'sheet1', u'sheet2'], sheet_captions=[u'GID'])

        ss.add_validator(integer_gid, 'insert_row', 'replace_row')

        row_validator = UniqueIntegerValidator2(u'GID')
        ss.add_validator(row_validator.insert, 'insert_row')
        ss.add_validator(row_validator.delete, 'delete_row')
        ss.add_validator(row_validator.replace, 'replace_row')

        sheet1 = ss[u'sheet1']
        sheet2 = ss[u'sheet2']

        sheet1.append([1])
        sheet1.append([2])
        self.assertRaises(ValidationError, sheet1.append, [2])
        self.assertRaises(ValidationError, sheet2.append, [2])

        del sheet1[1]
        sheet2.append([2])
        self.assertRaises(ValidationError, sheet1.append, [2])

        sheet2[0] = {u'GID': 3}
        sheet1.append([2])
