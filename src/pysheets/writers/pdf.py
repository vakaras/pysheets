#!/usr/bin/python


""" Writer for PDF files.
"""


import functools
import cStringIO

from xhtml2pdf.document import pisaDocument

from pysheets.writers import SheetWriter
from pysheets.writers.xhtml import XHTMLWriter


DOCUMENT_TEMPLATE = u"""
<!DOCTYPE HTML>
<html>
  <head>
    <title>{title}</title>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
  </head>
  <body>
    <div id="header" class="pdf">{header}</div>
    <div id="content">{content}</div>
    <div id="footer" class="pdf">{footer}</div>
  </body>
</html>
"""

DEFAULT_CSS = u"""

@font-face {
  font-family: ubuntu;
  src: url(/usr/share/fonts/truetype/ubuntu-font-family/Ubuntu-R.ttf);
}

@font-face {
  font-family: ubuntu;
  src: url(/usr/share/fonts/truetype/ubuntu-font-family/Ubuntu-B.ttf);
  font-weight: bold;
}

@font-face {
  font-family: ubuntu;
  src: url(/usr/share/fonts/truetype/ubuntu-font-family/Ubuntu-I.ttf);
  font-style: italic;
}

@font-face {
  font-family: ubuntu;
  src: url(/usr/share/fonts/truetype/ubuntu-font-family/Ubuntu-BI.ttf);
  font-weight: bold;
  font-style: italic;
}

@page {
  margin: 2cm;
  size: a4 portrait;
  @frame header{
    -pdf-frame-content: header;
    margin: 0.5cm;
  }
  @frame footer{
    -pdf-frame-content: footer;
    margin: 0.5cm;
    bottom: 0.5cm;
    height: 1cm;
  }
}

html {
  font-family: ubuntu;
  }
"""


class PDFWriter(SheetWriter):
    """ PDF file writer.
    """

    name = u'Portable document format'
    short_name = u'PDF'
    file_extensions = [u'pdf',]
    mime_type = 'application/pdf'

    def __init__(
            self, title=u'', header=u'', footer=u'', css=DEFAULT_CSS,
            *args, **kwargs):
        self.xhtml_writer = XHTMLWriter(*args, **kwargs)
        self.title = title
        self.header = header
        self.footer = footer
        self.css = css

    def write(self, sheet, file):
        """ Writes data from sheet into file.
        """

        table = cStringIO.StringIO()
        self.xhtml_writer(sheet, table)
        html_source = DOCUMENT_TEMPLATE.format(
                title=self.title,
                header=self.header,
                footer=self.footer,
                content=table.getvalue().decode('utf-8'))
        pdf = pisaDocument(
                html_source.encode('utf-8'), file, encoding='utf-8',
                default_css=self.css)

    @functools.wraps(write)
    def __call__(self, sheet, file):
        """ Wrapper function, which ensures that ``file`` is file like
        object.
        """

        if isinstance(file, unicode):
            with open(file, 'wb') as fp:
                self.write(sheet, fp)
        else:
            self.write(sheet, file)
