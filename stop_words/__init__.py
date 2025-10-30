import json
import os

from typing import Callable


CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
STOP_WORDS_DIR = os.path.join(CURRENT_DIR, "stop-words")
STOP_WORDS_CACHE: dict[str, list[str]] = {}

with open(os.path.join(STOP_WORDS_DIR, "languages.json"), "rb") as map_file:
    buffer = map_file.read()
    LANGUAGE_MAPPING = json.loads(buffer.decode("ascii"))

AVAILABLE_LANGUAGES = list(LANGUAGE_MAPPING.values())


def get_version() -> str:
    """
    :rtype: basestring
    """
    from ._version import __version__

    return __version__


class StopWordError(Exception):
    pass


def get_stop_words(language, cache: bool = True) -> list[str]:
    """
    :param language
    :param cache:
    :rtype: list
    """
    try:
        language = LANGUAGE_MAPPING[language]
    except KeyError:
        if language not in AVAILABLE_LANGUAGES:
            raise StopWordError('{0}" language is unavailable.'.format(language))

    if cache and language in STOP_WORDS_CACHE:
        return STOP_WORDS_CACHE[language]

    language_filename = os.path.join(STOP_WORDS_DIR, language + ".txt")
    try:
        with open(language_filename, "rb") as language_file:
            stop_words = [line.decode("utf-8").strip() for line in language_file.readlines()]
            stop_words = apply_filters(stop_words, language)
    except IOError:
        raise StopWordError('{0}" file is unreadable, check your installation.'.format(language_filename))

    if cache:
        STOP_WORDS_CACHE[language] = stop_words

    return stop_words[:]  # copy list, prevent being modified


_filters: dict[str | None, list[Callable]] = {None: []}


def apply_filters(stopwords: list[str], language: str) -> list[str]:
    """
    Apply registered filters to stopwords
    :param stopwords: list
    :param language: string
    :return: filtered stopwords
    """
    if language in _filters:
        for func in _filters[language]:
            stopwords = func(stopwords)

    for func in _filters[None]:
        stopwords = func(stopwords, language)

    return stopwords


def add_filter(func, language: str | None = None) -> None:
    """
    Register filters for specific language.
    If language == None the filter applies for all languages.
    Filter will not apply for stop words in cache.

    :param func: callable
    :param language: string|None
    :return:
    """
    if language not in _filters:
        _filters[language] = []
    _filters[language].append(func)


def remove_filter(func, language: str | None = None) -> bool:
    """
    :param func:
    :param language:
    :return:
    """
    if not (language in _filters and func in _filters[language]):
        return False
    _filters[language].remove(func)
    return True


def safe_get_stop_words(language: str) -> list[str]:
    """
    :type language: basestring

    :rtype: list
    """
    try:
        return get_stop_words(language)
    except StopWordError:
        return []
