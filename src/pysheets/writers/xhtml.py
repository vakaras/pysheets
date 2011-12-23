#!/usr/bin/python


""" Writer for xhtml tables.
"""


import datetime

from pysheets.writers import SheetWriter


class XHTMLWriter(SheetWriter):
    """ XHTML table writer.
    """

    name = u'XHTML'
    short_name = u'XHTML'
    file_extensions = [u'html', u'xhtml',]
    mime_type = 'application/xhtml+xml'

    def __init__(self, table_attrs=None, tr_attrs=None, td_attrs=None):
        self.table_attrs = table_attrs or {}
        self.tr_attrs = tr_attrs or {}
        self.td_attrs = td_attrs or {}

    def attributes_as_string(self, attributes):
        """ Converts attributes dict to string.
        """
        result = []
        for key, value in attributes.items():
            if isinstance(value, list):
                result.append(u'{0}=\"{1}\"'.format(key, u' '.join(value)))
            else:
                result.append(u'{0}=\"{1}\"'.format(key, value))
        return u' '.join(result)

    def write_row(self, row, write):
        """ Writes row, using ``write``.
        """

        write(u'  <tr {0}>'.format(
            self.attributes_as_string(self.tr_attrs)))
        for field in row:
            if isinstance(field, datetime.datetime):
                field = unicode(field.strftime('%Y-%m-%d %H:%M:%S'))
            elif isinstance(field, datetime.date):
                field = unicode(field.strftime('%Y-%m-%d'))
            elif not isinstance(field, unicode):
                field = unicode(field)
            write(u'<td {0}>{1}</td>'.format(
                self.attributes_as_string(self.td_attrs),
                field
                ))
        write(u'</tr>\n')

    def __call__(self, sheet, file):
        """ Writes data from sheet into file.
        """

        write = lambda text: file.write(text.encode('utf-8'))
        write(u'<table {0}>\n'.format(
            self.attributes_as_string(self.table_attrs)))
        write(u'  <tr {0}>'.format(
            self.attributes_as_string(self.tr_attrs)))
        for caption in sheet.captions:
            write(u'<th {0}>{1}</th>'.format(
                self.attributes_as_string(self.td_attrs),
                caption
                ))
        write(u'</tr>\n')
        for row in sheet:
            self.write_row(row, write)
        write(u'</table>\n')
