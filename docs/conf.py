#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sphinx_rtd_theme

from setupext import janitor


project = 'Setupext: janitor'
copyright = '2014, Dave Shawley'
version = janitor.__version__
release = janitor.__version__

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
