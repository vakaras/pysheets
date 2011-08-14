#!/usr/bin/python


import unittest

from pysheets.sheet import Row, Sheet


class RowTest(unittest.TestCase):
    """ Tests for :py:class:`pysheets.sheet.Row`.
    """

    def test_01(self):

        class DummySheet(object):
            """ Dummy class for Row testing.
            """

        sheet = DummySheet()

        row = Row(sheet, 0, [1, 2, 3])
        self.assertEqual(row.fields, [1, 2, 3])
        row.append("2")
        self.assertEqual(row.fields, [1, 2, 3, "2"])


class SheetTest(unittest.TestCase):
    """ Tests for :py:class:`pysheets.sheet.Sheet`.
    """

    def test_01(self):
        """ Good scenario.
        """

        sheet = Sheet(rows=[
            {u'a': 4, u'b': 5, u'c': 6},
            [4, 2, 3],
            [2, 4, 5],
            {u'c': u'haha', u'a': u'caca', u'b': u'dada'},
            [1, 7, 5],
            [3, 2, 5],
            ])
        self.assertEqual(len(sheet), 6)
        sheet.add_column('d', [1, 2, 3, 4, 5, 6])

    def test_02(self):
        """ Good scenario.
        """

        sheet = Sheet()
        self.assertEqual(sheet.captions, [])
        self.assertEqual(len(sheet), 0)
        self.assertEqual(sheet.rows, [])

        sheet.add_column(u'a')
        self.assertEqual(sheet.captions, [u'a'])
        self.assertEqual(sheet.captions_index, {u'a': 0})

        sheet.add_columns([u'b', u'c'])
        self.assertEqual(sheet.captions, [u'a', u'b', u'c'])
        self.assertEqual(sheet.captions_index, {u'a': 0, u'b': 1, u'c': 2})

        sheet.append_dict({u'a': 0, u'b': 1, u'c': 2})
        self.assertEqual(sheet.rows[0].fields, [0, 1, 2])

        sheet.append_iterable([2, 1, 3])
        self.assertEqual(sheet.rows[1].fields, [2, 1, 3])

        sheet.append(range(3))
        sheet.append({u'a': 'ddd', u'b': 'lll', u'c': (1, 2, 3)})

    def test_03(self):
        """ Good scenario.
        """

        sheet = Sheet(u'foo.csv', rows=[])
        self.assertEqual(sheet.captions, [])
        self.assertEqual(len(sheet), 0)
        self.assertEqual(sheet.rows, [])

    def test_04(self):
        """ Bad scenario.
        """

        sheet = Sheet()
        self.assertRaises(ValueError, sheet.append_iterable, [1, 2, 3])
        self.assertRaises(ValueError, sheet.add_column, u'a', [1])
