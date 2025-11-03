=================
Python Stop Words
=================

.. image:: https://img.shields.io/pypi/v/stop-words.svg
   :target: https://pypi.org/project/stop-words/
   :alt: PyPI version

.. image:: https://img.shields.io/pypi/pyversions/stop-words.svg
   :target: https://pypi.org/project/stop-words/
   :alt: Python versions

.. image:: https://img.shields.io/pypi/l/stop-words.svg
   :target: https://github.com/Alir3z4/python-stop-words/blob/master/LICENSE
   :alt: License

.. contents:: Table of Contents
   :depth: 2
   :local:

Overview
--------

A Python library providing curated lists of stop words across 34+ languages. Stop words are common words (like "the", "is", "at") that are typically filtered out in natural language processing and text analysis tasks.

**Key Features:**

* **34+ Languages** - Extensive language support.
* **Performance** - Built-in caching for fast repeated access.
* **Flexible** - Custom filtering system for advanced use cases.
* **Zero Dependencies** - Lightweight with no external requirements.


Available Languages
-------------------

All the available languages supported by https://github.com/Alir3z4/stop-words

Each language is identified by both its ISO 639-1 language code (e.g., ``en``) and full name (e.g., ``english``).


Installation
------------

**Via pip (Recommended):**

.. code-block:: bash

    $ pip install stop-words

**Via Git:**

.. code-block:: bash

    $ git clone --recursive https://github.com/Alir3z4/python-stop-words.git
    $ cd python-stop-words
    $ pip install -e .

**Requirements:**

* Usually any version of Python that supports type hints and probably has not been marked as EOL.


Quick Start
-----------

Basic Usage
~~~~~~~~~~~

.. code-block:: python

    from stop_words import get_stop_words

    # Get English stop words using language code
    stop_words = get_stop_words('en')
    
    # Or use the full language name
    stop_words = get_stop_words('english')
    
    # Use in text processing
    text = "The quick brown fox jumps over the lazy dog"
    words = text.lower().split()
    filtered_words = [word for word in words if word not in stop_words]
    print(filtered_words)  # ['quick', 'brown', 'fox', 'jumps', 'lazy', 'dog']


Safe Loading
~~~~~~~~~~~~

Use ``safe_get_stop_words()`` when you're not sure if a language is supported:

.. code-block:: python

    from stop_words import safe_get_stop_words

    # Returns empty list instead of raising an exception
    stop_words = safe_get_stop_words('klingon')  # Returns []
    
    # Works normally with supported languages
    stop_words = safe_get_stop_words('fr')  # Returns French stop words


Advanced Usage
--------------

Checking Available Languages
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from stop_words import AVAILABLE_LANGUAGES, LANGUAGE_MAPPING

    # List all available languages
    print(AVAILABLE_LANGUAGES)
    # ['arabic', 'bulgarian', 'catalan', ...]

    # View language code mappings
    print(LANGUAGE_MAPPING)
    # {'en': 'english', 'fr': 'french', ...}


Caching Control
~~~~~~~~~~~~~~~

By default, stop words are cached for performance. You can control this behavior:

.. code-block:: python

    from stop_words import get_stop_words, STOP_WORDS_CACHE

    # Disable caching for this call
    stop_words = get_stop_words('en', cache=False)
    
    # Clear the cache manually
    STOP_WORDS_CACHE.clear()
    
    # Check what's cached
    print(STOP_WORDS_CACHE.keys())  # ['english', 'french', ...]


Custom Filters
~~~~~~~~~~~~~~

Apply custom transformations to stop words using the filter system:

.. code-block:: python

    from stop_words import get_stop_words, add_filter, remove_filter

    # Add a global filter (applies to all languages)
    def remove_short_words(words, language):
        """Remove words shorter than 3 characters."""
        return [w for w in words if len(w) >= 3]
    
    add_filter(remove_short_words)
    stop_words = get_stop_words('en', cache=False)
    
    # Add a language-specific filter
    def uppercase_words(words):
        """Convert all words to uppercase."""
        return [w.upper() for w in words]
    
    add_filter(uppercase_words, language='english')
    stop_words = get_stop_words('en', cache=False)
    
    # Remove a filter when done
    remove_filter(uppercase_words, language='english')

**Note:** Filters only apply to newly loaded stop words, not cached ones. Use ``cache=False`` or clear the cache to apply new filters.


Practical Examples
------------------

Text Preprocessing
~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from stop_words import get_stop_words
    import re

    def preprocess_text(text, language='en'):
        """Clean and filter text for NLP tasks."""
        stop_words = set(get_stop_words(language))
        
        # Convert to lowercase and extract words
        words = re.findall(r'\b\w+\b', text.lower())
        
        # Remove stop words
        filtered_words = [w for w in words if w not in stop_words]
        
        return filtered_words

    text = "The quick brown fox jumps over the lazy dog"
    print(preprocess_text(text))
    # ['quick', 'brown', 'fox', 'jumps', 'lazy', 'dog']


Multilingual Processing
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from stop_words import get_stop_words

    def filter_multilingual_text(texts_dict):
        """Process texts in multiple languages.
        
        Args:
            texts_dict: Dictionary mapping language codes to text strings
        
        Returns:
            Dictionary with filtered words for each language
        """
        results = {}
        
        for lang_code, text in texts_dict.items():
            stop_words = set(get_stop_words(lang_code))
            words = text.lower().split()
            filtered = [w for w in words if w not in stop_words]
            results[lang_code] = filtered
        
        return results

    texts = {
        'en': 'The cat is on the table',
        'fr': 'Le chat est sur la table',
        'es': 'El gato está en la mesa'
    }
    
    print(filter_multilingual_text(texts))


Keyword Extraction
~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from stop_words import get_stop_words
    from collections import Counter
    import re

    def extract_keywords(text, language='en', top_n=10):
        """Extract the most common meaningful words from text."""
        stop_words = set(get_stop_words(language))
        
        # Extract words and filter
        words = re.findall(r'\b\w+\b', text.lower())
        meaningful_words = [w for w in words if w not in stop_words and len(w) > 2]
        
        # Count and return top keywords
        word_counts = Counter(meaningful_words)
        return word_counts.most_common(top_n)

    article = """
    Python is a high-level programming language. Python is known for its 
    simplicity and readability. Many developers choose Python for data science.
    """
    
    keywords = extract_keywords(article)
    print(keywords)
    # [('python', 3), ('language', 1), ('high-level', 1), ...]


API Reference
-------------

Functions
~~~~~~~~~

``get_stop_words(language, *, cache=True)``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Load stop words for a specified language.

**Parameters:**

* ``language`` (str): Language code (e.g., 'en') or full name (e.g., 'english')
* ``cache`` (bool, optional): Enable caching. Defaults to True.

**Returns:**

* ``list[str]``: List of stop words

**Raises:**

* ``StopWordError``: If language is unavailable or files are unreadable

**Example:**

.. code-block:: python

    stop_words = get_stop_words('en')
    stop_words = get_stop_words('french', cache=False)


``safe_get_stop_words(language)``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Safely load stop words, returning empty list on error.

**Parameters:**

* ``language`` (str): Language code or full name

**Returns:**

* ``list[str]``: Stop words, or empty list if unavailable

**Example:**

.. code-block:: python

    stop_words = safe_get_stop_words('unknown')  # Returns []


``add_filter(func, language=None)``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Register a filter function for stop word post-processing.

**Parameters:**

* ``func`` (Callable): Filter function
* ``language`` (str | None, optional): Language code or None for global filter

**Filter Signatures:**

* Language-specific: ``func(stopwords: list[str]) -> list[str]``
* Global: ``func(stopwords: list[str], language: str) -> list[str]``

**Example:**

.. code-block:: python

    def remove_short(words, lang):
        return [w for w in words if len(w) > 3]
    
    add_filter(remove_short)  # Global filter


``remove_filter(func, language=None)``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Remove a previously registered filter.

**Parameters:**

* ``func`` (Callable): The filter function to remove
* ``language`` (str | None, optional): Language code or None

**Returns:**

* ``bool``: True if removed, False if not found

**Example:**

.. code-block:: python

    success = remove_filter(my_filter, language='english')


Constants
~~~~~~~~~

``AVAILABLE_LANGUAGES``
^^^^^^^^^^^^^^^^^^^^^^^^

List of all supported language names.

.. code-block:: python

    ['arabic', 'bulgarian', 'catalan', ...]


``LANGUAGE_MAPPING``
^^^^^^^^^^^^^^^^^^^^

Dictionary mapping language codes to full names.

.. code-block:: python

    {'en': 'english', 'fr': 'french', 'de': 'german', ...}


``STOP_WORDS_CACHE``
^^^^^^^^^^^^^^^^^^^^^

Dictionary storing cached stop words. Can be manually cleared.

.. code-block:: python

    STOP_WORDS_CACHE.clear()  # Clear all cached data


Exceptions
~~~~~~~~~~

``StopWordError``
^^^^^^^^^^^^^^^^^

Raised when a language is unavailable or files cannot be read.

.. code-block:: python

    try:
        stop_words = get_stop_words('invalid')
    except StopWordError as e:
        print(f"Error: {e}")


Performance Tips
----------------

1. **Use caching** - Keep ``cache=True`` (default) for repeated access to the same language
2. **Reuse stop word sets** - Convert to ``set()`` once for O(1) lookup performance:

   .. code-block:: python

       stop_words_set = set(get_stop_words('en'))
       # Fast membership testing
       is_stop_word = 'the' in stop_words_set

3. **Preload languages** - Load stop words during initialization, not in tight loops
4. **Use safe_get_stop_words** - Avoid try/except overhead when language availability is uncertain


Troubleshooting
---------------

**"Language unavailable" error**

* Check spelling and use either the language code or full name
* Verify the language is in ``AVAILABLE_LANGUAGES``
* See the `Available Languages`_ table above

**"File is unreadable" error**

* Ensure the package installed correctly: ``pip install --force-reinstall stop-words``
* Check file permissions in the installation directory
* Verify the ``stop-words`` subdirectory exists in the package

**Filters not applying**

* Filters only affect newly loaded stop words
* Clear the cache: ``STOP_WORDS_CACHE.clear()``
* Use ``cache=False`` when testing filters

**Performance issues**

* Ensure caching is enabled (default behavior)
* Convert stop word lists to sets for faster lookups
* Preload stop words outside of loops


Contributing
------------

Contributions are welcome! Here's how you can help:

1. **Add new languages** - Submit stop word lists for unsupported languages via https://github.com/Alir3z4/stop-words
2. **Improve existing lists** - Suggest additions or removals for existing languages via https://github.com/Alir3z4/stop-words
3. **Report bugs** - Open issues on GitHub
4. **Submit PRs** - Fix bugs or add features

**Repository:** https://github.com/Alir3z4/python-stop-words


License
-------

This project is licensed under the BSD 3-Clause License. See ``LICENSE`` file for details.


Changelog
---------

See `ChangeLog.rst <https://github.com/Alir3z4/python-stop-words/blob/master/ChangeLog.rst>`_ for version history.


Support
-------

* **Issues:** https://github.com/Alir3z4/python-stop-words/issues
* **PyPI:** https://pypi.org/project/stop-words/


Credits
-------

* Maintained by `Alireza Savand <https://github.com/Alir3z4>`_
* Stop word lists compiled from various open sources
* Contributors: See `GitHub contributors <https://github.com/Alir3z4/python-stop-words/graphs/contributors>`_


Related Projects
----------------
* `Stop Words <https://github.com/Alir3z4/stop-words>`_ - List of common stop words in various languages.
* `NLTK <https://www.nltk.org/>`_ - Natural Language Toolkit with extensive NLP features
* `spaCy <https://spacy.io/>`_ - Industrial-strength NLP library
* `TextBlob <https://textblob.readthedocs.io/>`_ - Simplified text processing


Indices and Tables
------------------

* `Available Languages`_
* `Quick Start`_
* `Advanced Usage`_
* `API Reference`_
