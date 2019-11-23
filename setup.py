#!/usr/bin/env python
import setuptools

import setupext_janitor.janitor

setuptools.setup(
    name='setupext-janitor',
    version=setupext_janitor.version,
    author='Dave Shawley',
    author_email='daveshawley@gmail.com',
    url='http://github.com/dave-shawley/setupext-janitor',
    description='Making setup.py clean more useful.',
    long_description=open('README.rst').read(),
    packages=setuptools.find_packages(exclude=['tests', 'tests.*']),
    zip_safe=True,
    platforms='any',
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, != 3.4.*',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Framework :: Setuptools Plugin',
        'Development Status :: 5 - Production/Stable',
    ],
    entry_points={
        'distutils.commands': [
            'clean = setupext_janitor.janitor:CleanCommand',
        ],
    },
    cmdclass={
        'clean': setupext_janitor.janitor.CleanCommand,
    },
    extras_require={
        'dev': [
            'coverage==4.5.3',
            'flake8==3.7.7',
            'mock==1.0.1; python_version<"3"',
            'nose==1.3.7',
            'sphinx==1.8.5',
            'sphinx-rtd-theme==0.4.3',
            'tox==3.9.0',
        ],
    },
)
