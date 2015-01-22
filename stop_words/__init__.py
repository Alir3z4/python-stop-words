import os

__VERSION__ = (2015, 1, 19)
CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
STOP_WORDS_DIR = os.path.join(CURRENT_DIR, 'stop-words/')
STOP_WORDS_CACHE = {}

LANGUAGE_MAPPING = {
    'ar': 'arabic',
    'da': 'danish',
    'nl': 'dutch',
    'en': 'english',
    'fi': 'finnish',
    'fr': 'french',
    'de': 'german',
    'hu': 'hungarian',
    'it': 'italian',
    'nb': 'norwegian',
    'pt': 'portuguese',
    'ro': 'romanian',
    'ru': 'russian',
    'es': 'spanish',
    'sv': 'swedish',
    'tr': 'turkish',
}

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
        pass

    if language not in AVAILABLE_LANGUAGES:
        raise StopWordError('"%s" language is unavailable.' % language)

    if language in STOP_WORDS_CACHE:
        return STOP_WORDS_CACHE[language]

    try:
        language_filename = '{0}{1}.txt'.format(STOP_WORDS_DIR, language)
        with open(language_filename, 'rb') as language_file:
            stop_words = [line.strip().decode('utf-8')
                          for line in language_file.readlines()]
    except IOError:
        raise StopWordError(
            '"%s" file is unreadable, check your installation.' %
            language_filename)

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
