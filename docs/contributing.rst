Setting up your environment
---------------------------

The easiest way to start working with this code is to set up a virtual
environment and run ``env/bin/pip install -q '.[dev]'``.  That will install
the necessary testing and development tools.  Then you can run everything
else using ``env/bin/python setup.py``:

- *setup.py nosetest* will run the tests using nose to test against the
  and generate a coverage report to stdout.

- *setup.py build_sphinx* will generate HTML documentation into
  *build/doc/html*.  This is the doc set that is uploaded to Read The Docs.

- *setup.py flake8* will run the ``flake8`` utility and report on any
  static code analysis failures.

