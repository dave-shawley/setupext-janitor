from distutils import core, dist
from distutils.command import clean
import atexit
import os.path
import shutil
import sys
import tempfile
import uuid

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


class DirectoryCleanupMixin(object):

    @classmethod
    def setUpClass(cls):
        super(DirectoryCleanupMixin, cls).setUpClass()
        cls.temp_dir = tempfile.mkdtemp()
        atexit.register(shutil.rmtree, cls.temp_dir)

    @classmethod
    def create_directory(cls, dir_name):
        return tempfile.mkdtemp(dir=cls.temp_dir, prefix=dir_name)

    def assert_path_does_not_exist(self, *trailing_segments):
        full_path = os.path.join(*trailing_segments)
        if os.path.exists(full_path):
            raise AssertionError('{0} should not exist'.format(full_path))

    def assert_path_exists(self, *trailing_segments):
        full_path = os.path.join(*trailing_segments)
        if not os.path.exists(full_path):
            raise AssertionError('{0} should exist'.format(full_path))


class DistDirectoryCleanupTests(DirectoryCleanupMixin, unittest.TestCase):

    def test_that_dist_directory_is_removed_for_sdist(self):
        dist_dir = self.create_directory('dist-dir')
        run_setup(
            'sdist', '--dist-dir={0}'.format(dist_dir),
            'clean', '--dist',
        )
        self.assert_path_does_not_exist(dist_dir)

    def test_that_dist_directory_is_removed_for_bdist_dumb(self):
        dist_dir = self.create_directory('dist-dir')
        run_setup(
            'bdist_dumb', '--dist-dir={0}'.format(dist_dir),
            'clean', '--dist',
        )
        self.assert_path_does_not_exist(dist_dir)

    def test_that_multiple_dist_directories_with_be_removed(self):
        sdist_dir = self.create_directory('sdist-dir')
        bdist_dir = self.create_directory('bdist_dumb')
        run_setup(
            'sdist', '--dist-dir={0}'.format(sdist_dir),
            'bdist_dumb', '--dist-dir={0}'.format(bdist_dir),
            'clean', '--dist',
        )
        self.assert_path_does_not_exist(sdist_dir)
        self.assert_path_does_not_exist(bdist_dir)

    def test_that_directories_are_not_removed_without_parameter(self):
        sdist_dir = self.create_directory('sdist-dir')
        bdist_dir = self.create_directory('bdist_dumb')
        run_setup(
            'sdist', '--dist-dir={0}'.format(sdist_dir),
            'bdist_dumb', '--dist-dir={0}'.format(bdist_dir),
            'clean',
        )
        self.assert_path_exists(sdist_dir)
        self.assert_path_exists(bdist_dir)

    def test_that_directories_are_not_removed_in_dry_run_mode(self):
        sdist_dir = self.create_directory('sdist-dir')
        run_setup(
            'sdist', '--dist-dir={0}'.format(sdist_dir),
            'clean', '--dist', '--dry-run'
        )
        self.assert_path_exists(sdist_dir)


class EggDirectoryCleanupTests(DirectoryCleanupMixin, unittest.TestCase):

    def test_that_egg_info_directories_are_removed(self):
        egg_root = self.create_directory('egg-info-root')
        os.mkdir(os.path.join(egg_root, 'bah.egg-info'))
        os.mkdir(os.path.join(egg_root, 'foo.egg-info'))
        run_setup('clean', '--egg-base={0}'.format(egg_root), '--eggs')
        self.assert_path_exists(egg_root)
        self.assert_path_does_not_exist(egg_root, 'bah.egg-info')
        self.assert_path_does_not_exist(egg_root, 'foo.egg-info')

    def test_that_egg_directories_are_removed(self):
        dir_name = uuid.uuid4().hex + '.egg'
        os.mkdir(dir_name)
        try:
            run_setup('clean', '--eggs')
            self.assert_path_does_not_exist(dir_name)
        except:
            os.rmdir(dir_name)
            raise

    def test_that_directories_are_not_removed_in_dry_run_mode(self):
        egg_root = self.create_directory('egg-info-root')
        os.mkdir(os.path.join(egg_root, 'package.egg-info'))
        installed_egg = uuid.uuid4().hex + '.egg'
        os.mkdir(installed_egg)
        try:
            run_setup(
                'clean', '--egg-base={0}'.format(egg_root), '--eggs',
                '--dry-run',
            )
            self.assert_path_exists(installed_egg)
            self.assert_path_exists(egg_root, 'package.egg-info')
        except:
            os.rmdir(installed_egg)
            raise
        os.rmdir(installed_egg)
