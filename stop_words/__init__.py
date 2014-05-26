__VERSION__ = (2014, 5, 26)


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
    with open('stop-words/{}.txt'.format(language)) as lang_file:
        lines = lang_file.readlines()
        return [str(line.strip()).decode('utf-8') for line in lines]
