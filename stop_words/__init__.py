import os

__VERSION__ = (2014, 5, 26)
CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
STOP_WORDS_DIR = os.path.join(CURRENT_DIR, 'stop-words/')

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
        raise StopWordError('%s language is unavailable')

    try:
        with open('{0}{1}.txt'.format(STOP_WORDS_DIR, language)) as lang_file:
            lines = lang_file.readlines()
            return [str(line.strip()).decode('utf-8') for line in lines]
    except IOError:
        raise StopWordError('%s file is unreadable, check your installation')
