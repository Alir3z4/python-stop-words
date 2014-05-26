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
    package_data={
        'stop_words': [
            'stop-words/*.txt',
        ]
    },
    classifiers=[
        "Programming Language :: Python",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Topic :: Software Development"
    ],
)
