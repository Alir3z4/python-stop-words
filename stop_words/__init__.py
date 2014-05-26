__VERSION__ = (2014, 5, 26)


def get_version():
    """
    :rtype: basestring
    """
    return ".".join(str(v) for v in __VERSION__)
