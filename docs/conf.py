#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sphinx_rtd_theme

import setupext_janitor


project = 'Setupext: janitor'
copyright = '2014-2019, Dave Shawley'
version = setupext_janitor.version
release = setupext_janitor.version

needs_sphinx = '1.0'
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx',
    'sphinx.ext.viewcode',
]
templates_path = []
source_suffix = '.rst'
source_encoding = 'utf-8-sig'
master_doc = 'index'
pygments_style = 'sphinx'
html_theme = 'sphinx_rtd_theme'
html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]
html_static_path = []
exclude_patterns = []

intersphinx_mapping = {
    'python': ('http://docs.python.org/', None),
}
