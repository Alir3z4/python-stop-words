import os

__VERSION__ = (2014, 5, 26)
CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
STOP_WORDS_DIR = os.path.join(CURRENT_DIR, 'stop-words/')


def get_version():
    """
    :rtype: basestring
    """
    return ".".join(str(v) for v in __VERSION__)


def get_stop_words(language):
    """
    :type language: basestring

    :rtype: list
    """
    with open('{0}{1}.txt'.format(STOP_WORDS_DIR, language)) as lang_file:
        lines = lang_file.readlines()
        return [str(line.strip()).decode('utf-8') for line in lines]
