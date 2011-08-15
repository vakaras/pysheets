#!/usr/bin/python


import unittest

from pysheets.sheet import Row, Sheet, Column


class RowTest(unittest.TestCase):
    """ Tests for :py:class:`pysheets.sheet.Row`.
    """

    def test_01(self):

        class DummySheet(object):
            """ Dummy class for Row testing.
            """

        sheet = DummySheet()
        sheet.captions = [u'a', u'b', u'c']
        sheet.captions_index = dict([
            (v, i) for i, v in enumerate(sheet.captions)])

        row = Row(sheet, 0, [1, 2, 3])
        self.assertEqual(row.fields, [1, 2, 3])
        row.append(u'2')
        self.assertEqual(row.fields, [1, 2, 3, u'2'])

        self.assertEqual(list(row), [1, 2, 3, u'2'])
        self.assertEqual(row.keys(), [u'a', u'b', u'c'])
        self.assertEqual(row[u'b'], 2)
        row[u'b'] = 3
        self.assertEqual(row[u'b'], 3)


class ColumnTest(unittest.TestCase):
    """ Tests for :py:class:`pysheets.sheet.Column`.
    """

    def test_01(self):

        sheet = Sheet(captions=[u'a', u'b'], rows=[[1, 2], [3, 4], [5, 6],])
        col1, col2 = sheet.columns

        self.assertEqual(col1.caption, u'a')
        self.assertEqual(col1.index, 0)
        self.assertEqual(list(col1), [1, 3, 5])
        self.assertEqual(col2.caption, u'b')
        self.assertEqual(col2.index, 1)
        self.assertEqual(list(col2), [2, 4, 6])
        self.assertEqual(col1[1], 3)
        col1[1] = 10
        self.assertEqual(col1[1], 10)
        self.assertEqual(sheet[1][u'a'], 10)

        sheet.captions[1] = u'Foo'
        self.assertEqual(col2.caption, u'Foo')
        sheet.rows[1].fields[1] = 3
        self.assertEqual(list(col2), [2, 3, 6])


class SheetTest(unittest.TestCase):
    """ Tests for :py:class:`pysheets.sheet.Sheet`.
    """

    def test_01(self):
        """ Ok scenario.
        """

        sheet = Sheet(
                captions=[u'a', u'b', u'c'],
                rows=[
                    {u'a': 4, u'b': 5, u'c': 6},
                    [4, 2, 3],
                    [2, 4, 5],
                    {u'c': u'haha', u'a': u'caca', u'b': u'dada'},
                    [1, 7, 5],
                    [3, 2, 5],
                    ])
        self.assertEqual(len(sheet), 6)
        self.assertEqual(sheet.captions, [u'a', u'b', u'c'])

        self.assertEqual(list(sheet), sheet.rows)
        self.assertEqual(list(sheet[4]), [1, 7, 5])
        self.assertEqual(list(sheet[-2]), [1, 7, 5])
        self.assertEqual(
                [
                    u' '.join(unicode(field) for field in row)
                    for row in sheet[1::2]],
                [u'4 2 3', u'caca dada haha', u'3 2 5'])
        self.assertEqual(
                [
                    u' '.join(unicode(field) for field in row)
                    for row in sheet.filter(func=lambda x: x[u'c'] == 5)],
                [u'2 4 5', u'1 7 5', u'3 2 5'])
        self.assertEqual(
                list(sheet.get(u'c', u'a')),
                [[6, 4], [3, 4], [5, 2], [u'haha', u'caca'], [5, 1], [5, 3]]
                )

        sheet.add_column('d', [1, 2, 3, 4, 5, 6])
        column = sheet.get(u'd')
        self.assertEqual(column.index, 3)
        self.assertEqual(list(column), [1, 2, 3, 4, 5, 6])

        def compare(rows):
            self.assertEqual(
                    [
                        u' '.join(unicode(field) for field in row)
                        for row in sheet],
                    rows,)

        del sheet[3]
        compare([
            u'4 5 6 1', u'4 2 3 2', u'2 4 5 3', u'1 7 5 5', u'3 2 5 6'],)

        sheet.sort()
        compare([
            u'1 7 5 5', u'2 4 5 3', u'3 2 5 6', u'4 2 3 2', u'4 5 6 1'])
        sheet.sort(columns=[u'c', u'a'])
        compare([
            u'4 2 3 2', u'1 7 5 5', u'2 4 5 3', u'3 2 5 6', u'4 5 6 1'])
        sheet.sort(
                columns=[u'd', u'b'],
                cmp=lambda x, y: (x[u'b'] + x[u'd']) - (y[u'b'] + y[u'd']))
        compare([
            u'4 2 3 2', u'4 5 6 1', u'2 4 5 3', u'3 2 5 6', u'1 7 5 5'])
        sheet.sort(
                columns=[u'd', u'b'],
                key=lambda x: x[u'b'] + x[u'c'])
        compare([
            u'4 2 3 2', u'3 2 5 6', u'2 4 5 3', u'4 5 6 1', u'1 7 5 5'])
        sheet.sort(
                columns=[u'd', u'b'],
                key=lambda x: x[u'b'] + x[u'c'],
                reverse=True)
        compare([
            u'1 7 5 5', u'4 5 6 1', u'2 4 5 3', u'3 2 5 6', u'4 2 3 2'])

        sheet.sort([u'd'])
        sheet.remove(u'b')
        compare([u'4 6 1', u'4 3 2', u'2 5 3', u'1 5 5', u'3 5 6'],)
        sheet.remove(u'd')
        sheet.remove(u'a')
        compare([u'6', u'3', u'5', u'5', u'5'])
        sheet.remove(u'c')
        self.assertEqual(sheet.captions, [])
        self.assertEqual(len(sheet), 0)

    def test_02(self):
        """ Ok scenario.
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
        """ Ok scenario.
        """

        sheet = Sheet(u'foo.csv', rows=[])
        self.assertEqual(sheet.captions, [])
        self.assertEqual(len(sheet), 0)
        self.assertEqual(sheet.rows, [])

    def test_04(self):
        """ Failure scenario.
        """

        sheet = Sheet()
        self.assertRaises(ValueError, sheet.append_iterable, [1, 2, 3])
        self.assertRaises(ValueError, sheet.add_column, u'a', [1])

    def test_05(self):
        """ Ok scenario.
        """

        sheet = Sheet(rows=[
            {u'a': 1, u'b': 2},
            {u'a': 3, u'b': 4, u'c': 5},
            {u'a': 6, u'b': 7},])
        self.assertEqual(set(sheet.captions), set(u'ab'))
