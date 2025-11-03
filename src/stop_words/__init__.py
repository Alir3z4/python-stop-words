"""
Stop Words Library

A module for loading and managing stop words across multiple languages.
Stop words are common words that are typically filtered out in text processing.

This module provides:
- Loading stop words from language-specific files
- Caching for performance optimization
- Custom filtering system for post-processing stop words
- Language code mapping (e.g., 'en' -> 'english')
"""

import json
from pathlib import Path
from typing import Callable


# Directory configuration
CURRENT_DIR = Path(__file__).resolve().parent
STOP_WORDS_DIR = CURRENT_DIR / "stop-words"

# Global caches
STOP_WORDS_CACHE: dict[str, list[str]] = {}
_filters: dict[str | None, list[Callable[[list[str], str | None], list[str]]]] = {None: []}

# Load language mapping configuration
_languages_file = STOP_WORDS_DIR / "languages.json"
with _languages_file.open("r", encoding="utf-8") as f:
    LANGUAGE_MAPPING: dict[str, str] = json.load(f)

AVAILABLE_LANGUAGES: list[str] = list(LANGUAGE_MAPPING.values())


class StopWordError(Exception):
    """Raised when a requested language is unavailable or files are unreadable."""

    pass


def get_version() -> str:
    """
    Get the version of the stop words library.

    :returns: The version string from _version module.
    """
    from ._version import __version__  # type: ignore

    return __version__


def get_stop_words(language: str, *, cache: bool = True) -> list[str]:
    """
    Load stop words for a specified language.

    :param language: Language code (e.g., 'en', 'es') or full name (e.g., 'english', 'spanish').
        Supports both ISO codes and full language names via LANGUAGE_MAPPING.
    :param cache: If True, cache the results for faster subsequent access. Defaults to True.

    :returns: A list of stop words for the specified language. Returns a copy to prevent external modification.
    :raises StopWordError: If the language is not available or the file cannot be read.

    Example:
        >>> words = get_stop_words('en')
        >>> 'the' in words
        True
    """
    # Normalize language code to full name
    try:
        language = LANGUAGE_MAPPING[language]
    except KeyError:
        if language not in AVAILABLE_LANGUAGES:
            raise StopWordError(
                f'Language "{language}" is unavailable. '
                f'Available languages: {", ".join(sorted(AVAILABLE_LANGUAGES))}'
            )

    # Return cached version if available
    if cache and language in STOP_WORDS_CACHE:
        return STOP_WORDS_CACHE[language].copy()

    # Load stop words from file
    language_file = STOP_WORDS_DIR / f"{language}.txt"

    try:
        with language_file.open("r", encoding="utf-8") as f:
            stop_words = [line.strip() for line in f if line.strip()]
            stop_words = apply_filters(stop_words, language)
    except (IOError, OSError) as e:
        raise StopWordError(f'File "{language_file}" is unreadable. Check your installation. Error: {e}') from e

    # Cache if requested
    if cache:
        STOP_WORDS_CACHE[language] = stop_words

    return stop_words.copy()


def apply_filters(stopwords: list[str], language: str | None) -> list[str]:
    """
    Apply registered filters to stop words.

    Filters can modify, remove, or add stop words. Language-specific filters
    are applied first, followed by global filters (registered with language=None).

    :param stopwords: List of stop words to filter.
    :param language: Language code for language-specific filters.

    :returns: Filtered list of stop words.
    """
    # Apply language-specific filters
    if language in _filters:
        for func in _filters[language]:
            stopwords = func(stopwords, language)

    # Apply global filters
    for func in _filters[None]:
        stopwords = func(stopwords, language)

    return stopwords


def add_filter(func: Callable[[list[str], str | None], list[str]], *, language: str | None = None) -> None:
    """
    Register a filter function for stop word post-processing.

    Language-specific filters receive: func(stopwords: list[str]) -> list[str]
    Global filters receive: func(stopwords: list[str], language: str) -> list[str]

    Note: Filters only apply to newly loaded stop words, not cached ones.
          Clear the cache with STOP_WORDS_CACHE.clear() to reapply filters.

    :param func: Callable that takes a list of stop words and returns a modified list.
    :param language: Language code for language-specific filter, or None for global filter.

    Example:
        >>> # Add a filter to uppercase all stop words for English
        >>> add_filter(lambda words: [w.upper() for w in words], 'english')
        >>> # Add a global filter to remove single-character words
        >>> add_filter(lambda words, lang: [w for w in words if len(w) > 1])
    """
    if language is None:
        _filters[None].append(func)
        return

    if language not in _filters:
        _filters[language] = []

    _filters[language].append(func)


def remove_filter(func: Callable[[list[str], str | None], list[str]], *, language: str | None = None) -> bool:
    """
    Unregister a previously registered filter function.

    :param func: The filter function to remove.
    :param language: Language code or None for global filters.

    :returns: True if the filter was found and removed, False otherwise.
    """
    if language not in _filters or func not in _filters[language]:
        return False

    _filters[language].remove(func)
    return True


def safe_get_stop_words(language: str) -> list[str]:
    """
    Safely load stop words, returning an empty list on error.

    This is a convenience wrapper around get_stop_words() that catches
    StopWordError exceptions and returns an empty list instead.

    :param language: Language code or full name.

    :returns: Stop words for the language, or empty list if unavailable.

    Example:
        >>> words = safe_get_stop_words('unknown_language')
        >>> words
        []
    """
    try:
        return get_stop_words(language)
    except StopWordError:
        return []
