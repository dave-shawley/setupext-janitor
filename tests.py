from distutils import core, dist
from distutils.command import clean
import atexit
import os.path
import shutil
import sys
import tempfile

if sys.version_info >= (2, 7):
    import unittest
else:  # noinspection PyPackageRequirements,PyUnresolvedReferences
    import unittest2 as unittest

from setupext import janitor


def run_setup(*command_line):
    """
    Run the setup command with `command_line`.

    :param command_line: the command line arguments to pass
        as the simulated command line

    This function runs :func:`distutils.core.setup` after it
    configures an environment that mimics passing the specified
    command line arguments.  The ``distutils`` internals are
    replaced with a :class:`~distutils.dist.Distribution`
    instance that will only execute the clean command.  Other
    commands can be passed freely to simulate command line usage
    patterns.

    """
    class FakeDistribution(dist.Distribution):

        def __init__(self, *args, **kwargs):
            """Enable verbose output to make tests easier to debug."""
            dist.Distribution.__init__(self, *args, **kwargs)
            self.verbose = 3

        def run_command(self, command):
            """Only run the clean command."""
            if command == 'clean':
                dist.Distribution.run_command(self, command)

        def parse_config_files(self, filenames=None):
            """Skip processing of configuration files."""
            pass

    core.setup(
        distclass=FakeDistribution,
        script_name='testsetup.py',
        script_args=command_line,
        cmdclass={'clean': janitor.CleanCommand},
    )


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


class DirectoryCleanupTests(unittest.TestCase):
    temp_dir = tempfile.mkdtemp()

    @classmethod
    def setUpClass(cls):
        super(DirectoryCleanupTests, cls).setUpClass()
        atexit.register(shutil.rmtree, cls.temp_dir)

    @classmethod
    def create_directory(cls, dir_name):
        full_path = os.path.join(cls.temp_dir, dir_name)
        os.mkdir(full_path)
        return full_path

    def assert_path_does_not_exist(self, full_path):
        if os.path.exists(full_path):
            raise AssertionError('{0} should not exist'.format(full_path))

    def test_that_dist_directory_is_removed_for_sdist(self):
        dist_dir = self.create_directory('dist-dir')
        run_setup(
            'sdist', '--dist-dir={0}'.format(dist_dir),
            'clean', '--dist',
        )
        self.assert_path_does_not_exist(dist_dir)
