from distutils.command import clean
import sys

if sys.version_info >= (2, 7):
    import unittest
else:
    import unittest2 as unittest

from setupext import janitor


class CommandOptionTests(unittest.TestCase):

    def test_that_distutils_options_are_present(self):
        defined_options = set(t[0] for t in janitor.CleanCommand.user_options)
        superclass_options = set(t[0] for t in clean.clean.user_options)
        self.assertTrue(defined_options.issuperset(superclass_options))

    def test_that_janitor_user_options_are_not_clean_options(self):
        self.assertIsNot(
            janitor.CleanCommand.user_options, clean.clean.user_options)

    def test_that_janitor_defines_dist_command(self):
        self.assertIn(
            ('dist', 'd', 'remove distribution directory'),
            janitor.CleanCommand.user_options)
