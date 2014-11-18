#!/usr/bin/env python
import codecs
import setuptools
import sys

from setupext import janitor


with codecs.open('README.rst', 'rb', encoding='utf-8') as file_obj:
    long_description = '\n' + file_obj.read()

install_requirements = []
test_requirements = ['nose>1.3,<2']
if sys.version_info < (3, ):
    test_requirements.append('mock>1.0,<2')
if sys.version_info < (2, 7):
    test_requirements.append('unittest2')


setuptools.setup(
    name='setupext-janitor',
    version=janitor.__version__,
    author='Dave Shawley',
    author_email='daveshawley@gmail.com',
    url='http://github.com/dave-shawley/setupext-janitor',
    description='Making setup.py clean more useful.',
    long_description=long_description,
    packages=setuptools.find_packages(exclude=['tests', 'tests.*']),
    namespace_packages=['setupext'],
    zip_safe=True,
    platforms='any',
    install_requires=install_requirements,
    tests_require=test_requirements,
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Setuptools Plugin',
        'Development Status :: 3 - Alpha',
    ],
    entry_points={
        'distutils.commands': [
            'clean = setupext.janitor:CleanCommand',
        ],
    },
    cmdclass={
        'clean': janitor.CleanCommand,
    },
)
