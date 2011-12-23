#!/usr/bin/python


import unittest
import os
import datetime
import tempfile
from cStringIO import StringIO

from pysheets.exceptions import IntegrityError, InvalidFileError
from pysheets.writers.xhtml import XHTMLWriter
from pysheets.sheet import Sheet


class XHTMLWriterTest(unittest.TestCase):
    """ Tests for :py:class:`pysheets.writers.xhtml.XHTMLWriter`.
    """

    def setUp(self):

        self.sheet = Sheet(
                captions=[u'Number', u'Square', u'Cube'],
                rows=[(i, i * i, i * i * i) for i in range(5)]
                )
        self.file = StringIO()

    def test_01(self):

        writer = XHTMLWriter()
        writer(self.sheet, self.file)
        self.assertEqual(
                self.file.getvalue(),
                """\
<table >
  <tr ><th class="col0">Number</th><th class="col1">Square</th><th class="col2">Cube</th></tr>
  <tr ><td class="col0">0</td><td class="col1">0</td><td class="col2">0</td></tr>
  <tr ><td class="col0">1</td><td class="col1">1</td><td class="col2">1</td></tr>
  <tr ><td class="col0">2</td><td class="col1">4</td><td class="col2">8</td></tr>
  <tr ><td class="col0">3</td><td class="col1">9</td><td class="col2">27</td></tr>
  <tr ><td class="col0">4</td><td class="col1">16</td><td class="col2">64</td></tr>
</table>
"""
                )

    def test_02(self):

        writer = XHTMLWriter(
                table_attrs={'class': ['grey', 'blue'], 'id': 'class1'},
                tr_attrs={'c': ['y', 'r',]},
                td_attrs={'c': ['b', 'o',]},
                )
        writer(self.sheet, self.file)
        self.assertEqual(
                self.file.getvalue(),
                """\
<table class="grey blue" id="class1">
  <tr c="y r"><th c="b o" class="col0">Number</th><th c="b o" class="col1">Square</th><th c="b o" class="col2">Cube</th></tr>
  <tr c="y r"><td c="b o" class="col0">0</td><td c="b o" class="col1">0</td><td c="b o" class="col2">0</td></tr>
  <tr c="y r"><td c="b o" class="col0">1</td><td c="b o" class="col1">1</td><td c="b o" class="col2">1</td></tr>
  <tr c="y r"><td c="b o" class="col0">2</td><td c="b o" class="col1">4</td><td c="b o" class="col2">8</td></tr>
  <tr c="y r"><td c="b o" class="col0">3</td><td c="b o" class="col1">9</td><td c="b o" class="col2">27</td></tr>
  <tr c="y r"><td c="b o" class="col0">4</td><td c="b o" class="col1">16</td><td c="b o" class="col2">64</td></tr>
</table>
"""
                )
