import json
import os

__VERSION__ = (2015, 2, 21)
CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
STOP_WORDS_DIR = os.path.join(CURRENT_DIR, 'stop-words')
STOP_WORDS_CACHE = {}

with open(os.path.join(STOP_WORDS_DIR, 'languages.json'), 'rb') as map_file:
    buffer = map_file.read()
    buffer = buffer.decode('ascii')
    LANGUAGE_MAPPING = json.loads(buffer)

AVAILABLE_LANGUAGES = LANGUAGE_MAPPING.values()


def get_version():
    """
    :rtype: basestring
    """
    return ".".join(str(v) for v in __VERSION__)


class StopWordError(Exception):
    pass


def get_stop_words(language):
    """
    :type language: basestring

    :rtype: list
    """
    try:
        language = LANGUAGE_MAPPING[language]
    except KeyError:
        if language not in AVAILABLE_LANGUAGES:
            raise StopWordError('{0}" language is unavailable.'.format(
                language
            ))

    if language in STOP_WORDS_CACHE:
        return STOP_WORDS_CACHE[language]

    language_filename = os.path.join(STOP_WORDS_DIR, language + '.txt')
    try:
        with open(language_filename, 'rb') as language_file:
            stop_words = [line.decode('utf-8').strip()
                          for line in language_file.readlines()]
    except IOError:
        raise StopWordError(
            '{0}" file is unreadable, check your installation.'.format(
                language_filename
            )
        )

    STOP_WORDS_CACHE[language] = stop_words

    return stop_words


def safe_get_stop_words(language):
    """
    :type language: basestring

    :rtype: list
    """
    try:
        return get_stop_words(language)
    except StopWordError:
        return []
