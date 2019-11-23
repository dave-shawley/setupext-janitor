Changelog
=========

* Next release

  - Add support for *--build* (`#17`_)
  - Clean up sphinx generated directories with *--build* (`#6`_)

* 1.1.1 (07-May-2019)

  - Fix ``Requires-Python`` metadata.

* 1.1.0 (07-May-2019)

  - Drop support for Python 2.6, and 3.0-3.4
  - Move `version` and `version_info` from the `janitor` module into the
    top-level package.  Also renamed `__version__` to `version`
  - Remove namespace packaging (thanks @ionelmc)
  - Fix distribution cleanup on Windows (thanks @maphew)
  - Clean up *.eggs* as well as *.egg* (thanks @maphew)
  - Switch from pypip.in to shields.io (thanks @movermeyer)

* 1.0.0 (19-Nov-2014)

  - Support removal of virtual environment directories.
  - Support recursive removal of *__pycache__* directories.
  - Add support for *--all*.
  - Support removal of .egg-info and .egg directories.
  - Add support for *--dry-run*
  - Support removal of distribution directories.


.. _#6: https://github.com/dave-shawley/setupext-janitor/issues/6
.. _#17: https://github.com/dave-shawley/setupext-janitor/issues/17
