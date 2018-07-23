2018.7.23
=========

* Fixed #14: `languages.json` is missing, if you don't git clone with `--recursive`.
* Feature: Support latest version of Python (3.7+).
* Feature #22: Enforces packaging of eggs into folders.
* Update the `stop-words` repository to get the latest languages.
* Fixed Travis failing and tests due to bootstrap.


2015.2.23.1
===========

* Fixed #9: Missing ``languages.json`` file that breaks the installation.


2015.2.23
=========

* Feature: Using the cache is optional
* Feature: Filtering stopwords

2015.2.21
=========

* Feature: ``LANGUAGE_MAPPING`` is loads from stop-words/languages.json
* Fixed: Made paths OS-independent


2015.1.31
=========

* Feature #5: Decode error AND Add ``catalan`` language to ``LANGUAGE_MAPPING`.
* Feature: Update `stop-words` dictionary.


2015.1.22
=========

* Feature: Tests
* Feature: Python 3 support
* Feature: Dev installation via zc.buildout
* Feature: Continuous integration via Travis


2015.1.19
=========

* Feature #3: Handle language code, cache and custom errors 


2014.5.26
=========

* Initial release.
* Package on pypi.
* github.com/Alir3z4/stop-words as submodule.

