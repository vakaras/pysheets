=========
Use-cases
=========

Working with CSV file
=====================

>>> from pysheets.sheet import Sheet

--------------
Importing data
--------------

File type can be recognized automatically by file extension, or specified 
explicitly by name or class:

>>> from cStringIO import StringIO
>>> data = StringIO('''
... "Name";"E-mail";"Phone numbers"
... "Foo Bar";"foo@example.com";"+37060000000;+37061111111"
... "Fooer Barer";"bar@example.com";"+37062222222"
... ''')
>>> sheet = Sheet(data, u'CSV')

--------------------------
Examples of accessing data
--------------------------

Printing all column captions:

>>> for caption in sheet.captions:
...     print caption
Name
E-mail
Phone

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

>>> for phones, name in sheet.get(u'Phone', u'Name'):
...     print name, phones
Foo Bar +37060000000;+37061111111
Fooer Barer +37062222222

Iterating through rows:

>>> print u', '.join(caption for caption in sheet.captions)
... for row in sheet:
...     print u', '.join(field for field in row)
Name, E-mail, Phone numbers
Foo Bar, foo@example.com, +37060000000;+37061111111
Fooer Barer, bar@example.com, +37062222222

Acessing single row:

>>> print u', '.join(field for field in sheet[1])
Fooer Barer, bar@example.com, +37062222222

Negative index and slices works like with normal :py:class:`list`:

>>> print u', '.join(field for field in sheet[-1])
Fooer Barer, bar@example.com, +37062222222

Accessing single cell:

>>> row = sheet[0]
>>> print row[u'Name']
Foo Bar
>>> column = sheet.get(u'Name')
>>> print column[0]
Foo Bar
>>> print sheet.get(u'Name')[1]
Fooer Barer
>>> print sheet.get(u'Name')[1] is sheet[1][u'Name']
True

Filtering:

>>> filtered_sheet = Sheet(rows=sheet.filter(lambda x: x.index >= 1))

--------------------------
Examples of modifying data
--------------------------

Changing value of single cell:

>>> row = u'Ba Ba'
>>> print row[u'Name'], column[0], sheet.get(u'Name')[0]
Ba Ba Ba Ba Ba Ba
>>> column[0] = u'Ta Ta'
>>> print row[u'Name'], column[0], sheet.get(u'Name')[0]
Ta Ta Ta Ta Ta Ta
>>> sheet.get(u'Name')[0] = u'Foo Bar'
>>> print row[u'Name'], column[0], sheet.get(u'Name')[0]
Foo Bar Foo Bar Foo Bar

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
...     u'E-mail': u'foo@bar.com',
...     u'Phone numbers': u'+37063333333'}
>>> sheet.get(u'Name')[1]
Fooer Barer

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
>>> sheet.sort(columns=[u'E-mail', u'Name'])
...                                     # Firstly sorts by email, than by 
...                                     # name.
>>> sheet.sort(key=lambda x: x[u'Name'])
...                                     # If key or cmp is passed, then it
...                                     # is used instead of columns.

Deleting column:

>>> sheet.remove(u'Name')

Deleting row:

>>> del sheet[0]

-----------------------
Examples of adding data
-----------------------

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
... 
... class UniqueIntegerValidator(object):
...     
...     def __init__(self, column):
...         self.values = set()
...         self.column = column
...         
...     def insert(self, sheet, row):
...         try:
...             row[column] = int(row[column])
...         except ValueError:
...             raise ValidationError((
...                 u'Values of column {0} have to be integers.'
...                 ).format(column))
...         if value in self.values:
...             raise ValidationError((
...                 u'Values of column {0} have to be unique integers.'
...                 ).format(column))
...         else:
...             self.values.add(row[column])
...         return row
...             
...     def delete(self, sheet, row):
...         self.remove(row[column])
...     
...     def replace(self, sheet, row, replaced_row):
...         self.delete(sheet, replaced_row)
...         self.insert(sheet, row)
...         return row

>>> validator = UniqueIntegerValidator('ID')
>>> sheet = Sheet()
>>> sheet.add_insert_validator(validator.insert)
>>> sheet.insert_validators
[<bound method UniqueIntegerValidator.insert of <....UniqueIntegerValidator object at 0x...>>]
>>> sheet.add_delete_validator(validator.delete)
>>> sheet.delete_validators
[<bound method UniqueIntegerValidator.delete of <....UniqueIntegerValidator object at 0x...>>]
>>> sheet.add_replace_validator(validator.replace)
>>> sheet.replace_validators
[<bound method UniqueIntegerValidator.replace of <....UniqueIntegerValidator object at 0x...>>]

>>> sheet.add_column(u'ID')
>>> sheet.append(["baba"])
Traceback (most recent call last):
...
ValidationError: Values of column ID have to be integers.
>>> len(sheet)
0
>>> sheet.append([u'2'])
>>> sheet.append([u'3'])
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
>>> sheet.append([u'3'])
>>> sheet[1] = {u'ID': 4}
>>> sheet.append([u'3'])

>>> def split_name(sheet, row, replaced_row=None):
...     row['First name'], row['Last name'] = row[u'Name'].split()
...     del row[u'Name']
...     return row
>>> sheet = Sheet()
>>> sheet.add_insert_validator(split_name)
>>> sheet.add_replace_validator(split_name)
>>> sheet.add_columns([u'First name', u'Last name'])
>>> sheet.read(data, u'CSV',
...            create_columns=True)     # Create columns, which doesn't 
...                                     # exist.
>>> print u' '.join(sorted(sheet.captions))
E-mail First name Last name Phone numbers
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

---------------------
Joining and splitting
---------------------

>>> sheet = Sheet()
>>> sheet.add_columns([u'Type', u'Number'])
>>> for i in range(20):
...     sheet.append([i % 3, i])
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
>>> types = sheet.split(u'Type')        # Unicode or tuple of unicodes.
>>> for key, rows in types.items():
...     print key, u', '.join(row[u'ID'] for row in rows)
0 0, 3, 6, 9, 12, 15, 18
1 1, 4, 7, 10, 13, 16, 19
2 2, 5, 8, 11, 14, 17

>>> ss = SpreadSheet()
>>> for tab, rows in types.items():
...     ss[unicode(tab)] = Sheet(rows=rows)
>>> sheet = ss.join(u'NewType')
>>> print sorted(sheet.captions)
[u'ID', u'NewType', u'Type']
