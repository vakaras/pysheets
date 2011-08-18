#!/usr/bin/python


import unittest

from pysheets.plugins import PluginManager, MountPoint


class PluginManagerTest(unittest.TestCase):
    """ Tests for :py:class:`pysheets.plugins.PluginManager`.
    """

    def test_01(self):

        class Plugin01(object):
            short_name = u'plugin01'
            file_extensions = [u'xyz', u'dvq']
            mime_type = u'text/plg'

        class Plugin02(Plugin01):
            short_name = u'plugin02'
            file_extensions = [u'xyz', u'dvq']
            mime_type = u'text/plg'

        manager = PluginManager()
        self.assertEqual(len(manager), 0)

        manager.add(Plugin01)
        self.assertEqual(len(manager), 1)
        self.assertIs(manager[u'plugin01'], Plugin01)
        self.assertRaises(KeyError, manager.__getitem__, u'plugin02')
        self.assertIs(manager.get_by_extension(u'xyz'), Plugin01)
        self.assertIs(manager.get_by_file(u'bla.xyz'), Plugin01)
        self.assertIs(manager.get_by_file(u'fsfd/dff/bla.xyz'), Plugin01)
        self.assertRaises(KeyError, manager.get_by_file, u'bla.tar.xyz')
        self.assertIs(manager.get_by_mime('text/plg'), Plugin01)

        manager.add(Plugin02)
        self.assertEqual(len(manager), 2)
        self.assertIs(manager[u'plugin01'], Plugin01)
        self.assertIs(manager[u'plugin02'], Plugin02)
        self.assertIs(manager.get_by_extension(u'xyz'), Plugin02)
        self.assertIs(manager.get_by_file(u'bla.xyz'), Plugin02)
        self.assertIs(manager.get_by_file(u'fsfd/dff/bla.xyz'), Plugin02)
        self.assertRaises(KeyError, manager.get_by_file, u'bla.tar.xyz')
        self.assertIs(manager.get_by_mime('text/plg'), Plugin02)


class MountPointTest(unittest.TestCase):
    """ Tests for :py:class:`pysheets.plugins.MountPoint`.
    """

    def test_01(self):

        class BasePlugin(object):

            __metaclass__ = MountPoint

        manager = BasePlugin.plugins
        self.assertTrue(isinstance(manager, PluginManager))
        self.assertEqual(len(manager), 0)

        class Plugin01(BasePlugin):
            short_name = u'plugin01'
            file_extensions = [u'xyz', u'dvq']
            mime_type = u'text/plg'

        self.assertEqual(len(manager), 1)
        self.assertIs(manager[u'plugin01'], Plugin01)
        self.assertRaises(KeyError, manager.__getitem__, u'plugin02')
        self.assertIs(manager.get_by_extension(u'xyz'), Plugin01)
        self.assertIs(manager.get_by_file(u'bla.xyz'), Plugin01)
        self.assertIs(manager.get_by_file(u'fsfd/dff/bla.xyz'), Plugin01)
        self.assertRaises(KeyError, manager.get_by_file, u'bla.tar.xyz')
        self.assertIs(manager.get_by_mime('text/plg'), Plugin01)

        class Plugin02(Plugin01):
            short_name = u'plugin02'
            file_extensions = [u'xyz', u'dvq']
            mime_type = u'text/plg'

        self.assertEqual(len(manager), 2)
        self.assertIs(manager[u'plugin01'], Plugin01)
        self.assertIs(manager[u'plugin02'], Plugin02)
        self.assertIs(manager.get_by_extension(u'xyz'), Plugin02)
        self.assertIs(manager.get_by_file(u'bla.xyz'), Plugin02)
        self.assertIs(manager.get_by_file(u'fsfd/dff/bla.xyz'), Plugin02)
        self.assertRaises(KeyError, manager.get_by_file, u'bla.tar.xyz')
        self.assertIs(manager.get_by_mime('text/plg'), Plugin02)
