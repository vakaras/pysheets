#!/usr/bin/python


"""

:py:class:`SpreadSheet` is a dict of :py:class:`sheets <Sheet>`
"""


from pysheets.exceptions import IntegrityError
from pysheets.sheet import Sheet


class SpreadSheet(object):
    """ Class representing a dict of sheets.

    .. py:attribute:: names

        List of sheets names.

    """

    def __init__(
            self, file=None, reader_name=None, reader=None, names=None,
            reader_args=None, sheet_captions=None):
        """

        If ``file`` is not ``None``, then data is read from it.

        If ``reader_name`` and ``reader`` is None, then it is expected
        that file is an unicode string with path to a file to read
        information from and which reader to use is tried to guess by
        file name extension.

        If ``names`` is not ``None``, then sheets with given names are
        created. If ``sheet_captions`` is not ``None`` too, then it is
        passed to :py:class:`sheet's <Sheet>` constructor.

        :param file: File from which to read data.
        :type file: unicode or file like object.
        :param reader_name: Name of the reader to use.
        :type reader_name: None or unicode.
        :param reader: Callable to use for reading file.
        :type reader: None or callable.

        """

        self.names = []
        self.sheets = {}

        self.validator_creators = []
        self.validators = {
                'insert_row': [],
                'delete_row': [],
                'replace_row': [],
                'add_sheet': [],
                'remove_sheet': [],
                }

        if names:
            self.create_sheets(names, captions=sheet_captions)

    def __len__(self):
        return len(self.sheets)

    def __iter__(self):
        for name in self.names:
            yield self.sheets[name]

    def __getitem__(self, name):
        return self.sheets[name]

    def __delitem__(self, name):

        sheet = self.sheets[name]

        for validator in self.validators['remove_sheet']:
            validator(self, name, sheet)

        sheet.unset_spreadsheet()
        del self.sheets[name]
        self.names.remove(name)

    def create_sheet(self, name, *args, **kwargs):
        """ Creates sheet and appends it to spreadsheet with given name.

        ``args`` and ``kwargs`` are passed to :py:class:`Sheet`
        constructor.

        :param name: The name of the Sheet.
        :type name: unicode
        :returns: Created sheet.

        """

        sheet = Sheet(*args, **kwargs)
        for validator_creator in self.validator_creators:
            for validator, validator_type in zip(
                    validator_creator(),
                    ['insert', 'delete', 'replace']):
                if validator is not None:
                    sheet.add_validator(validator, validator_type)

        for validator in self.validators['add_sheet']:
            sheet, name = validator(self, name, sheet)

        if name in self.sheets:
            raise IntegrityError(
                    u'Sheet with name \"{0}\" already exists.'.format(name))
        else:
            self.sheets[name] = sheet
            self.names.append(name)
            sheet.set_spreadsheet(self, name)

            return sheet

    def create_sheets(self, names, *args, **kwargs):
        """ Creates sheets and appends them to spreadsheet.

        ``args`` and ``kwargs`` are passed to :py:class:`Sheet`
        constructor.

        """

        for name in names:
            self.create_sheet(name, *args, **kwargs)

    def add_sheet_validator_creator(self, validator_creator):
        """

        ``validator_creator`` have to be callable, which returns
        tuple of 3 validators (some of which can be ``None``):

        +   row insert validator;
        +   row delete validator;
        +   row replace validator.

        For each sheet ``validator_creator`` is called and validators
        are appended to sheet validators lists.

        """

        self.validator_creators.append(validator_creator)

        for sheet in self:
            for validator, validator_type in zip(
                    validator_creator(), ['insert', 'delete', 'replace']):
                if validator is not None:
                    sheet.add_validator(validator, validator_type)

    def add_sheet_validator(self, validator, *types):
        """ Adds validator to each sheet validators lists mentioned in
        ``types``.
        """


        def validator_creator():
            """ Validator creator, which just returns given validator.
            """

            return [validator if validator_type in types else None
                    for validator_type in ['insert', 'delete', 'replace']]

        self.add_sheet_validator_creator(validator_creator)

    def add_validator(self, validator, *types):
        """ Adds validator to validators lists mentioned in ``types``.

        .. note::
            Validators are just added. They are not executed for
            existing data.
        """

        for validator_type in types:
            self.validators[validator_type].append(validator)

    def validate_row_insertion(self, sheet, row):
        """ Executes ``insert_row`` validators.
        """

        for validator in self.validators['insert_row']:
            row = validator(self, sheet, row)
        return row

    def validate_row_deletion(self, sheet, row):
        """ Executes ``delete_row`` validators.
        """

        for validator in self.validators['delete_row']:
            row = validator(self, sheet, row)
        return row

    def validate_row_replacement(self, sheet, row, replaced_row):
        """ Executes ``replace_row`` validators.
        """

        for validator in self.validators['replace_row']:
            row = validator(self, sheet, row, replaced_row)
        return row