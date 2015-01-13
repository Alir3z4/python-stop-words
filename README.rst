=================
Python Stop Words
=================

Get list of common stop words in various languages in Python.

Available languages
-------------------

* Arabic
* Danish
* Dutch
* English
* Finnish
* French
* German
* Hungarian
* Italian
* Norwegian
* Portuguese
* Romanian
* Russian
* Spanish
* Swedish
* Turkish


Installation
------------
``stop-words`` is available on PyPi

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

    stop_words = get_stop_words('english')
