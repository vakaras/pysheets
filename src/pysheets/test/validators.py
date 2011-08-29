#!/usr/bin/python


""" Validators used by tests.
"""


class ValidationError(Exception):
    pass


class UniqueIntegerValidator(object):

    def __init__(self, column):
        self.values = set()
        self.column = column

    def insert(self, sheet, row):
        try:
            value = row[self.column] = int(row[self.column])
        except ValueError:
            raise ValidationError((
                u'Values of column {0} have to be integers.'
                ).format(self.column))
        if value in self.values:
            raise ValidationError((
                u'Values of column {0} have to be unique integers.'
                ).format(self.column))
        else:
            self.values.add(value)
        return row

    def delete(self, sheet, row):
        self.values.remove(row[self.column])

    def replace(self, sheet, row, replaced_row):
        self.delete(sheet, replaced_row)
        return self.insert(sheet, row)


class UniqueNameValidator(object):
    """ Validates if all names in list are unique.
    """

    def __init__(self):
        self.values = set()
        self.counter = 1

    def insert(self, sheet, row):
        value = (row[u'First name'], row[u'Last name'])
        if value in self.values:
            raise ValidationError(u'Name duplicate')
        else:
            self.values.add(value)
        row.setdefault(u'ID', unicode(self.counter))
        self.counter += 1
        return row

    def delete(self, sheet, row):
        self.values.remove((row[u'First name'], row[u'Last name']))

    def replace(self, sheet, row, replaced_row):
        self.delete(sheet, replaced_row)
        return self.insert(sheet, row)


def unique_integer_validator_creator():
    """ Returns unique integer validator.
    """

    validator = UniqueIntegerValidator(u'ID')
    return (validator.insert, validator.delete, validator.replace)


def validate_nothing(sheet, row, replaced_row=None):
    """ A dummy function for testing.
    """
    return row
