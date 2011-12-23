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
  <tr ><th >Number</th><th >Square</th><th >Cube</th></tr>
  <tr ><td >0</td><td >0</td><td >0</td></tr>
  <tr ><td >1</td><td >1</td><td >1</td></tr>
  <tr ><td >2</td><td >4</td><td >8</td></tr>
  <tr ><td >3</td><td >9</td><td >27</td></tr>
  <tr ><td >4</td><td >16</td><td >64</td></tr>
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
  <tr c="y r"><th c="b o">Number</th><th c="b o">Square</th>\
<th c="b o">Cube</th></tr>
  <tr c="y r"><td c="b o">0</td><td c="b o">0</td><td c="b o">0</td></tr>
  <tr c="y r"><td c="b o">1</td><td c="b o">1</td><td c="b o">1</td></tr>
  <tr c="y r"><td c="b o">2</td><td c="b o">4</td><td c="b o">8</td></tr>
  <tr c="y r"><td c="b o">3</td><td c="b o">9</td><td c="b o">27</td></tr>
  <tr c="y r"><td c="b o">4</td><td c="b o">16</td><td c="b o">64</td></tr>
</table>
"""
                )
