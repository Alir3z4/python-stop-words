=================
Python Stop Words
=================

.. contents:: Table of contents

Overview
--------

Get list of common stop words in various languages in Python.

.. image:: https://secure.travis-ci.org/Alir3z4/python-stop-words.png
   :alt: Build Status
   :target: http://travis-ci.org/Alir3z4/python-stop-words

.. image:: https://coveralls.io/repos/Alir3z4/python-stop-words/badge.png
   :alt: Coverage Status
   :target: https://coveralls.io/r/Alir3z4/python-stop-words


.. image:: http://badge.kloud51.com/pypi/v/stop-words.svg
    :target: https://pypi.python.org/pypi/stop-words
    :alt: PyPI Version

.. image:: http://badge.kloud51.com/pypi/w/stop-words.svg
    :target: https://pypi.python.org/pypi/stop-words
    :alt: PyPI Wheel

.. image:: http://badge.kloud51.com/pypi/s/stop-words.svg
    :target: https://pypi.python.org/pypi/stop-words
    :alt: PyPI Status

.. image:: http://badge.kloud51.com/pypi/l/stop-words.svg
    :target: https://github.com/Alir3z4/python-stop-words/blob/master/LICENSE
    :alt: License

.. image:: http://badge.kloud51.com/pypi/f/stop-words.svg
    :target: https://pypi.python.org/pypi/stop-words
    :alt: PyPI Format

.. image:: http://badge.kloud51.com/pypi/p/stop-words.svg
    :target: https://pypi.python.org/pypi/stop-words
    :alt: PyPI Py_versions

.. image:: http://badge.kloud51.com/pypi/d/stop-words.svg
    :target: https://pypi.python.org/pypi/stop-words
    :alt: PyPI Downloads

.. image:: http://badge.kloud51.com/pypi/i/stop-words.svg
    :target: https://pypi.python.org/pypi/stop-words
    :alt: PyPI Implementation

.. image:: http://badge.kloud51.com/pypi/e/stop-words.svg
    :target: https://pypi.python.org/pypi/stop-words
    :alt: PyPI Egg


Available languages
-------------------

* Arabic
* Bulgarian
* Catalan
* Czech
* Danish
* Dutch
* English
* Finnish
* French
* German
* Hungarian
* Indonesian
* Italian
* Norwegian
* Polish
* Portuguese
* Romanian
* Russian
* Spanish
* Swedish
* Turkish
* Ukrainian


Installation
------------
``stop-words`` is available on PyPI

http://pypi.python.org/pypi/stop-words

So easily install it by ``pip``
::

    $ pip install stop-words

Or by ``easy_install``
::

    $ easy_install stop-words

Another way is by cloning ``stop-words``'s `git repo <https://github.com/Alir3z4/python-stop-words>`_ ::

    $ git clone git://github.com/Alir3z4/python-stop-words.git

Then install it by running:
::

    $ python setup.py install


Basic usage
-----------
::

    from stop_words import get_stop_words

    stop_words = get_stop_words('en')
    stop_words = get_stop_words('english')

    from stop_words import safe_get_stop_words

    stop_words = safe_get_stop_words('unsupported language')

Python compatibility
--------------------

Python-stop-words has been originally developed for Python 2, but has been
ported and tested for Python 3.
