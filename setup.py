from setuptools import setup, find_packages

setup(
    name='stop-words',
    version=__import__("stop_words").get_version(),
    description='Get list of common stop words in various languages in Python',
    long_description=open('README.rst').read(),
    license=open('LICENSE').read(),
    author='Alireza Savand',
    author_email='alireza.savand@gmail.com',
    url='https://github.com/Alir3z4/python-stop-words',
    packages=find_packages(),
    zip_safe=False,
    package_data={
        'stop_words': [
            'stop-words/*.txt',
            'stop-words/languages.json',
        ]
    },
    classifiers=[
        'Programming Language :: Python',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Topic :: Software Development',
        'Development Status :: 6 - Mature',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Text Processing',
        'Topic :: Text Processing :: Filters',
        'License :: OSI Approved :: BSD License',
    ],
)
