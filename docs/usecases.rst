=========
Use-cases
=========

--------------
Importing data
--------------

File type can be recognized automatically by file extension, or specified 
explicitly by name or class:

>>> from cStringIO import StringIO
>>> from pysheets.sheet import Sheet
>>> data = StringIO('''\
... "Name";"E-Mail";"Phone numbers"
... "Foo Bar";"foo@example.com";"+37060000000;+37061111111"
... "Fooer Barer";"bar@example.com";"+37062222222"\
... ''')
>>> sheet = Sheet(data, u'CSV')
>>> sheet.captions
[u'Name', u'E-Mail', u'Phone numbers']
>>> for row in sheet:
...     print list(row)
[u'Foo Bar', u'foo@example.com', u'+37060000000;+37061111111']
[u'Fooer Barer', u'bar@example.com', u'+37062222222']


--------------------------
Examples of accessing data
--------------------------

Printing all column captions:

>>> from pysheets.sheet import Sheet
>>> sheet = Sheet(
...     captions=[u'Name', u'E-mail', u'Phone numbers'],
...     rows=[
...         [u'Foo Bar', u'foo@example.com', u'+37060000000;+37061111111',],
...         [u'Fooer Barer', u'bar@example.com', u'+37062222222'],])

>>> for caption in sheet.captions:
...     print caption
Name
E-mail
Phone numbers

Iterating through columns:

>>> for column in sheet.columns:
...     print column.caption, u', '.join(column)
Name Foo Bar, Fooer Barer
E-mail foo@example.com, bar@example.com
Phone numbers +37060000000;+37061111111, +37062222222

Accessing data in single column by column name:

>>> for name in sheet.get(u'Name'):
...     print name
Foo Bar
Fooer Barer

Accessing data in multiple columns:

>>> for phones, name in sheet.get(u'Phone numbers', u'Name'):
...     print name, phones
Foo Bar +37060000000;+37061111111
Fooer Barer +37062222222

Iterating through rows:

>>> print u', '.join(sheet.captions)
Name, E-mail, Phone numbers
>>> for row in sheet:
...     print u', '.join(row)
Foo Bar, foo@example.com, +37060000000;+37061111111
Fooer Barer, bar@example.com, +37062222222

Acessing single row:

>>> print u', '.join(sheet[1])
Fooer Barer, bar@example.com, +37062222222

Negative index and slices works like with normal :py:class:`list`:

>>> print u', '.join(sheet[-1])
Fooer Barer, bar@example.com, +37062222222
>>> print u'\n'.join(u', '.join(row) for row in sheet[1:])
Fooer Barer, bar@example.com, +37062222222

Accessing single cell:

>>> row = sheet[0]
>>> print row[u'Name']
Foo Bar
>>> column = list(sheet.get(u'Name'))
>>> print column[0]
Foo Bar
>>> print list(sheet.get(u'Name'))[1]
Fooer Barer
>>> print list(sheet.get(u'Name'))[1] is sheet[1][u'Name']
True

Filtering:

>>> filtered_sheet = Sheet(
...     rows=sheet.filter(lambda x: u'2' in x[u'Phone numbers']))

--------------------------
Examples of modifying data
--------------------------

Changing value of single cell:

>>> sheet = Sheet(
...     captions=[u'Name', u'E-Mail', u'Phone numbers'],
...     rows=[
...         [u'Foo Bar', u'foo@example.com', u'+37060000000;+37061111111',],
...         [u'Fooer Barer', u'bar@example.com', u'+37062222222'],
...         [u'Arer Fooer', u'h@example.com', u'+37064444444'],
...         [u'Murer Zuer', u'l@example.com', u'+37063333333'],
...         [u'Other Random Name', u'abba@example.com', u'+37065555555'],
...         [u'Random Name', u'k@example.com', u'+37067777777'],
...         [u'Random Name', u'dddd@example.com', u'+37066666666'],
...         ])
>>> row = sheet[0]
>>> column = sheet.get(u'Name')

>>> row[u'Name'] = u'Ba Ba'
>>> print row[u'Name'], column[0], list(sheet.get(u'Name'))[0]
Ba Ba Ba Ba Ba Ba
>>> column[0] = u'Ta Ta'
>>> print row[u'Name'], column[0], sheet.get(u'Name')[0]
Ta Ta Ta Ta Ta Ta
>>> sheet.get(u'Name')[0] = u'Foo Bar'
>>> print row[u'Name'], column[0], sheet.get(u'Name')[0]
Foo Bar Foo Bar Foo Bar

..
    Changing entire column:

    >>> from pysheets.column import Column
    >>> column = Column([u'Ta Ta', u'Ba Ba'])
    >>> print column.caption                # Column is not associated with
    ...                                     # sheet yet.
    None
    >>> sheet.set(u'Name', column)
    >>> print column.caption                # Now column is associated.
    Name
    >>> print sheet.get(u'Name')[1]
    Ba Ba

Changing entire row:

>>> sheet[0] = {
...     u'Name': u'Fooer Barer',
...     u'E-Mail': u'foo@bar.com',
...     u'Phone numbers': u'+37063333333'}
>>> sheet.get(u'Name')[1]
u'Fooer Barer'
>>> sheet[0] = {
...     u'Name': u'Foo Bar',
...     u'E-Mail':  u'foo@example.com',
...     u'Phone numbers': u'+37060000000;+37061111111',}

..
    Copying row:

    >>> for name in sheet.get(u'Name'):
    ...     print name
    Fooer Barer
    Ba Ba
    >>> sheet[1] = sheet[0]
    >>> for name in sheet.get(u'Name'):
    ...     print name
    Fooer Barer
    Fooer Barer

Sorting:

>>> sheet.sort()                        # Sorts in captions order.
...                                     # (Firstly by name, then by email
...                                     # and so on.)
>>> for row in sheet:
...     print u', '.join(row)
Arer Fooer, h@example.com, +37064444444
Foo Bar, foo@example.com, +37060000000;+37061111111
Fooer Barer, bar@example.com, +37062222222
Murer Zuer, l@example.com, +37063333333
Other Random Name, abba@example.com, +37065555555
Random Name, dddd@example.com, +37066666666
Random Name, k@example.com, +37067777777

>>> sheet.sort(columns=[u'E-Mail', u'Name'])
...                                     # Firstly sorts by email, than by 
...                                     # name.
>>> for row in sheet:
...     print u', '.join(row)
Other Random Name, abba@example.com, +37065555555
Fooer Barer, bar@example.com, +37062222222
Random Name, dddd@example.com, +37066666666
Foo Bar, foo@example.com, +37060000000;+37061111111
Arer Fooer, h@example.com, +37064444444
Random Name, k@example.com, +37067777777
Murer Zuer, l@example.com, +37063333333

>>> sheet.sort(key=lambda x: x[u'Name'])
...                                     # If key or cmp is passed, then it
...                                     # is used instead of columns.
>>> for row in sheet:
...     print u', '.join(row)
Arer Fooer, h@example.com, +37064444444
Foo Bar, foo@example.com, +37060000000;+37061111111
Fooer Barer, bar@example.com, +37062222222
Murer Zuer, l@example.com, +37063333333
Other Random Name, abba@example.com, +37065555555
Random Name, dddd@example.com, +37066666666
Random Name, k@example.com, +37067777777

Deleting column:

>>> sheet.remove(u'Name')
>>> sheet.captions
[u'E-Mail', u'Phone numbers']
>>> for row in sheet:
...     print u', '.join(row)
h@example.com, +37064444444
foo@example.com, +37060000000;+37061111111
bar@example.com, +37062222222
l@example.com, +37063333333
abba@example.com, +37065555555
dddd@example.com, +37066666666
k@example.com, +37067777777

.. warning::
    All :py:class:`columns <Column>` are corrupted, when any column is 
    removed from sheet.

    >>> column = sheet.get(u'Phone numbers')
    >>> column.caption
    u'Phone numbers'
    >>> sheet.remove(u'E-Mail')
    >>> column.caption
    Traceback (most recent call last):
    ...
    IndexError: list index out of range

Deleting row:

>>> del sheet[1]
>>> for row in sheet:
...     print u', '.join(row)
+37064444444
+37062222222
+37063333333
+37065555555
+37066666666
+37067777777

-----------------------
Examples of adding data
-----------------------

>>> from pysheets.sheet import Sheet
>>> sheet = Sheet()

Adding empty columns:

>>> sheet.add_column(u'name')
>>> sheet.add_columns([u'email', u'phone'])
>>> len(sheet)
0

Adding rows:

>>> sheet.append([u'Foo Bar', u'foo@bar.com', u'+37060000000'])
>>> sheet.append({
...     u'name': u'Fooer Bar',
...     u'email': u'fooer@bar.com',
...     u'phone': u'+37060000000',
...     })
>>> len(sheet)
2

Adding columns with data:

>>> sheet.add_column(u'Gender', [u'M', u'M'])
>>> len(sheet)
2

------------------------
Validators and modifiers
------------------------

Validators (modifiers) are executed each time, when a row is **added**,  
**replaced** or **deleted** from the sheet. They are executed in order
in which they appears in validators queue.

>>> class ValidationError(Exception):
...     pass

>>> class UniqueIntegerValidator(object):
...     
...     def __init__(self, column):
...         self.values = set()
...         self.column = column
...         
...     def insert(self, sheet, row):
...         try:
...             value = row[self.column] = int(row[self.column])
...         except ValueError:
...             raise ValidationError((
...                 u'Values of column {0} have to be integers.'
...                 ).format(self.column))
...         if value in self.values:
...             raise ValidationError((
...                 u'Values of column {0} have to be unique integers.'
...                 ).format(self.column))
...         else:
...             self.values.add(value)
...         return row
...             
...     def delete(self, sheet, row):
...         self.values.remove(row[self.column])
...     
...     def replace(self, sheet, row, replaced_row):
...         self.delete(sheet, replaced_row)
...         return self.insert(sheet, row)

>>> validator = UniqueIntegerValidator('ID')
>>> sheet = Sheet()
>>> sheet.add_insert_validator(validator.insert)
>>> sheet.insert_validators
[<bound method UniqueIntegerValidator.insert of <UniqueIntegerValidator object at 0x...>>]
>>> sheet.add_delete_validator(validator.delete)
>>> sheet.delete_validators
[<bound method UniqueIntegerValidator.delete of <UniqueIntegerValidator object at 0x...>>]
>>> sheet.add_replace_validator(validator.replace)
>>> sheet.replace_validators
[<bound method UniqueIntegerValidator.replace of <UniqueIntegerValidator object at 0x...>>]

>>> sheet.add_column(u'ID')
>>> sheet.append(["baba"])
Traceback (most recent call last):
...
ValidationError: Values of column ID have to be integers.
>>> len(sheet)
0
>>> sheet.append([u'2'])
>>> sheet.append([u'3'])
>>> sorted(validator.values)
[2, 3]
>>> sheet[1][u'ID']
3
>>> len(sheet)
2
>>> sheet.append([3])
Traceback (most recent call last):
...
ValidationError: Values of column ID have to be unique integers.

>>> len(sheet)
2
>>> del sheet[1]
>>> for i, row in enumerate(sheet):
...     print i, u', '.join(unicode(field) for field in row)
0 2
>>> validator.values
set([2])
>>> sheet.append([u'3'])
>>> sheet[1] = {u'ID': 4}
>>> sheet.append([u'3'])

>>> def split_name(sheet, row, replaced_row=None):
...     row['First name'], row['Last name'] = row[u'Name'].split()
...     del row[u'Name']
...     return row
>>> sheet = Sheet(captions=[u'First name', u'Last name'])
>>> sheet.add_insert_validator(split_name)
>>> sheet.add_replace_validator(split_name)

>>> from cStringIO import StringIO
>>> data = StringIO('''\
... "Name";"E-Mail";"Phone numbers"
... "Foo Bar";"foo@example.com";"+37060000000;+37061111111"
... "Fooer Barer";"bar@example.com";"+37062222222"\
... ''')
>>> sheet.read(data, reader_name=u'CSV',
...            create_columns=False)    # Create columns, which doesn't
...                                     # exist.
>>> print u' '.join(sorted(sheet.captions))
First name Last name
>>> for row in sheet:
...     print u', '.join(row)
Foo, Bar
Fooer, Barer
>>> sheet.append({
...     u'Name': u'Bla bla',
...     u'E-mail': u'b@g.com',
...     u'Phone numbers': u''})
>>> sheet.get(u'First name')[-1]
u'Bla'
>>> sheet[-1] = {
...     u'Name': u'Ku Foo',
...     u'E-mail': u'b@g.com',
...     u'Phone numbers': u''}
>>> sheet.get(u'Last name')[-1]
u'Foo'

.. note::
    When using modifiers, which change columns, only rows in dict
    format should be used:

    >>> sheet.append([u'Foo Bar'] * 4)
    Traceback (most recent call last):
    ...
    ValueError: Columns number mismatch. Expected 5. Is 4.

*Behind the scene*: A row, which is not associated with sheet is just a
simple Python :py:class:`dict`, which if passed all validators is converted
to :py:class:`pysheets.Row` object and added to sheet.

-------------------
Readers and writers
-------------------

A **Reader** have to be a class inherited from
:py:class:`readers.SheetReader` and it should define:

+   ``name`` – unicode string, the full name of reader (this will be used,
    when displaying messages to users);
+   ``short_name`` – unique (between readers) unicode string (it is used
    as reader identifier);
+   ``file_extensions`` – tuple of unicode strings (used for file type
    guessing);
+   ``mime_type`` – byte string;
+   ``read(sheet, file, create_columns, **kwargs)`` – method, which
    extracts data from file and adds it to sheet.


A **Writer** have to be a class inherited from
:py:class:`writers.SheetWriter` and it should define:

+   ``name`` – unicode string, the full name of writer (this will be used,
    when displaying messages to users);
+   ``short_name`` – unique (between writers) unicode string (it is used
    as writer identifier);
+   ``file_extensions`` – tuple of unicode strings (used for file type
    guessing);
+   ``mime_type`` – byte string;
+   ``write(sheet, file, **kwargs)`` – method, which
    extracts data from file and adds it to sheet.

-----------
SpreadSheet
-----------

>>> from pysheets.spreadsheet import SpreadSheet
>>> ss = SpreadSheet()
>>> ss.names
[]
>>> len(ss)
0
>>> sheet = ss.create_sheet(u'sheet1')
>>> ss.names
[u'sheet1']
>>> len(ss)
1
>>> list(ss) == [sheet]
True
>>> sheet.spreadsheet is ss
True
>>> sheet.name
u'sheet1'
>>> ss[u'sheet1'] is sheet
True

Adding validators to all sheets:

>>> def validator_creator():
...     validator = UniqueIntegerValidator(u'ID')
...     return validator.insert, validator.delete, validator.replace
>>> ss.add_sheet_validator_creator(validator_creator)
>>> ss.add_sheet_validator(split_name, 'insert', 'replace')

>>> sheet.insert_validators
[<bound method UniqueIntegerValidator.insert of <UniqueIntegerValidator object at 0x...>>, <function split_name at 0x...>]
>>> sheet.delete_validators
[<bound method UniqueIntegerValidator.delete of <UniqueIntegerValidator object at 0x...>>]
>>> sheet.replace_validators
[<bound method UniqueIntegerValidator.replace of <UniqueIntegerValidator object at 0x...>>, <function split_name at 0x...>]

Adding spreadsheet validators:

>>> def integer_gid(spreadsheet, sheet, row, replaced_row=None):
...     try:
...         row[u'GID'] = int(row[u'GID'])
...     except ValueError:
...         raise ValidationError((
...             u'Values of column {0} have to be integers.'
...             ).format(self.column))
...     return row
>>> ss.add_validator(integer_gid, 'insert_row', 'replace_row')

>>> class UniqueIntegerValidator2(object):
...
...     def __init__(self, column):
...         self.values = set()
...         self.column = column
...
...     def insert(self, spreadsheet, sheet, row):
...         value = row[self.column]
...         if value in self.values:
...             raise ValidationError((
...                 u'Values of column {0} have to be unique integers.'
...                 ).format(self.column))
...         else:
...             self.values.add(value)
...         return row
...
...     def delete(self, spreadsheet, sheet, row):
...         self.values.remove(row[self.column])
...
...     def replace(self, spreadsheet, sheet, row, replaced_row):
...         self.delete(spreadsheet, sheet, replaced_row)
...         return self.insert(spreadsheet, sheet, row)


>>> row_validator = UniqueIntegerValidator2(u'GID')
>>> ss.add_validator(row_validator.insert, 'insert_row')
>>> ss.add_validator(row_validator.delete, 'delete_row')
>>> ss.add_validator(row_validator.replace, 'replace_row')

>>> sheet1 = ss[u'sheet1']
>>> sheet1.add_columns([
...     u'ID', u'GID', u'First name', u'Last name'])
>>> sheet2 = ss.create_sheet(
...     u'sheet2',
...     captions=[u'ID', u'GID', u'First name', u'Last name'])
>>> sheet1.append({u'ID': 1, u'GID': 1, u'Name': u'Foo Bar'})
>>> sheet1.append({u'ID': 2, u'GID': 2, u'Name': u'Foo Bar'})
>>> sheet1.append({u'ID': 2, u'GID': 3, u'Name': u'Foo Bar'})
Traceback (most recent call last):
...
ValidationError: Values of column ID have to be unique integers.
>>> sheet2.append({u'ID': 4, u'GID': 4, u'Name': u'Foo Bar'})
>>> sheet2.append({u'ID': 4, u'GID': 3, u'Name': u'Foo Bar'})
Traceback (most recent call last):
...
ValidationError: Values of column ID have to be unique integers.
>>> sheet2.append({u'ID': 3, u'GID': 3, u'Name': u'Foo Bar'})
>>> sheet2.append({u'ID': 2, u'GID': 2, u'Name': u'Foo Bar'})
Traceback (most recent call last):
...
ValidationError: Values of column GID have to be unique integers.

>>> class SheetOrder(object):
...
...     def __init__(self):
...         self.numbers = set()
...
...     def add(self, spreadsheet, name, sheet):
...         number = int(name)
...         if number != max(self.numbers or [0]) + 1:
...             raise ValidationError(u'Wrong sheet name.')
...         else:
...             self.numbers.add(number)
...         return sheet, unicode(number)
...
...     def remove(self, spreadsheet, name, sheet):
...         number = int(name)
...         if number != max(self.numbers):
...             raise ValidationError(u'Cannot remove sheet.')
...         else:
...             self.numbers.remove(number)

>>> ss2 = SpreadSheet()
>>> sheet_validator = SheetOrder()
>>> ss2.add_validator(sheet_validator.add, 'add_sheet')
>>> ss2.add_validator(sheet_validator.remove, 'remove_sheet')
>>> ss2.create_sheet(u'sheet1')
Traceback (most recent call last):
...
ValueError: invalid literal for int() with base 10: 'sheet1'
>>> ss2.create_sheet(u'    1   ').name
u'1'
>>> ss2.create_sheet(u'  1        \t   ')
Traceback (most recent call last):
...
ValidationError: Wrong sheet name.
>>> ss2.create_sheet(2).name
u'2'
>>> del ss2[u'1']
Traceback (most recent call last):
...
ValidationError: Cannot remove sheet.
>>> sheet = ss2[u'2']
>>> del ss2[u'2']
>>> print sheet.name
None

---------------------
Joining and splitting
---------------------

>>> sheet = Sheet()
>>> sheet.add_columns([u'Type', u'Number'])
>>> for i in range(20):
...     sheet.append([i % 3, unicode(i)])
>>> for tp, num in sheet:
...     print tp, num
0 0
1 1
2 2
0 3
1 4
2 5
0 6
1 7
2 8
0 9
1 10
2 11
0 12
1 13
2 14
0 15
1 16
2 17
0 18
1 19
>>> ss = SpreadSheet()
>>> ss.load(sheet, u'Type')
>>> for sheet in ss:
...     print [sheet.name, u', '.join(row[u'Number'] for row in sheet)]
[u'0', u'0, 3, 6, 9, 12, 15, 18']
[u'1', u'1, 4, 7, 10, 13, 16, 19']
[u'2', u'2, 5, 8, 11, 14, 17']

>>> sheet = ss.join(u'NewType')
>>> print sorted(sheet.captions)
[u'NewType', u'Number', u'Type']

--------------
Exporting data
--------------

>>> from pysheets.spreadsheet import SpreadSheet
>>> from pysheets.sheet import Sheet
>>>
>>> sheet = Sheet(
...     captions=[u'Type', u'Number', u'Square'],
...     rows=[(i%3, i, i * i) for i in range(20)])
...
>>> ss = SpreadSheet()
>>> ss.load(sheet, columns=u'Type')
>>> ss.write('/tmp/example.ods')
