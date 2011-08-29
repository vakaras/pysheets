#!/usr/bin/python


""" Plugin architecture based on idea described
`here <http://martyalchin.com/2008/jan/10/simple-plugin-framework/>`_.
"""


import os


class PluginManager(object):
    """ Takes care of all plugins.
    """

    def __init__(self):
        self.plugins = {}
        self.file_extensions = {}
        self.mime_types = {}

    def __getitem__(self, short_name):
        return self.plugins[short_name]

    def __len__(self):
        return len(self.plugins)

    def add(self, cls):
        """ Registers plugin.

        Plugin class must have these attributes:

        +   ``short_name`` -- unicode string, unique identifier;
        +   ``file_extension`` -- iterable of unicode strings;
        +   ``mime_type``.
        """

        self.plugins[cls.short_name] = cls
        for file_extension in cls.file_extensions:
            self.file_extensions.setdefault(file_extension, []).append(cls)
        self.mime_types.setdefault(cls.mime_type, []).append(cls)

    def get_by_extension(self, extension):
        """ Returns last registered plugin, which can handle file with
        given extension.
        """

        return self.file_extensions[extension][-1]

    def get_by_file(self, filename):
        """ Returns plugin, which can handle file with given filename.
        (Guessing based on file name extension.)
        """

        extension = os.extsep.join(
                os.path.basename(filename).split(os.extsep)[1:])
        return self.get_by_extension(extension)

    def get_by_mime(self, mime_type):
        """ Returns last registered plugin, which can handle file with
        given mime type.
        """

        return self.mime_types[mime_type][-1]


class MountPoint(type):
    """ Meta class for readers and writers plugin mount point.
    """

    def __init__(mcs, name, bases, attrs):
        """

        +   If creating mount point class, then creates plugins dict.
        +   If creating plugin, then ads it to plugins dict. Attribute
            ``short_name`` is used as dict key.

        """

        super(MountPoint, mcs).__init__(name, bases, attrs)

        if not hasattr(mcs, 'plugins'):
            mcs.plugins = PluginManager()
        else:
            mcs.plugins.add(mcs)
