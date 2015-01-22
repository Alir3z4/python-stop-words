"""
Tests for stop-words
"""
from unittest import TestCase
from unittest import TestSuite
from unittest import TestLoader

import stop_words
from stop_words import StopWordError
from stop_words import get_stop_words
from stop_words import safe_get_stop_words
from stop_words import STOP_WORDS_CACHE


class StopWordsTestCase(TestCase):
    number_of_english_stop_words = 174

    def test_get_stop_words(self):
        sw = get_stop_words('english')
        self.assertEqual(len(sw), self.number_of_english_stop_words)

    def test_get_stop_words_language_mapping(self):
        sw = get_stop_words('en')
        self.assertEqual(len(sw), self.number_of_english_stop_words)
        self.assertEqual(sw, get_stop_words('english'))

    def test_get_stop_words_cache(self):
        self.assertFalse('french' in STOP_WORDS_CACHE)
        sw = get_stop_words('fr')
        self.assertTrue('french' in STOP_WORDS_CACHE)
        original_stop_words_dir = stop_words.STOP_WORDS_DIR
        stop_words.STOP_WORDS_DIR = '/trash/'
        self.assertEqual(sw, get_stop_words('french'))
        stop_words.STOP_WORDS_DIR = original_stop_words_dir
        try:
            get_stop_words('klingon')
        except:
            pass
        self.assertFalse('klingon' in STOP_WORDS_CACHE)

    def test_get_stop_words_unavailable_language(self):
        self.assertRaises(StopWordError, get_stop_words, 'sindarin')

    def test_get_stop_words_install_issue(self):
        original_stop_words_dir = stop_words.STOP_WORDS_DIR
        stop_words.STOP_WORDS_DIR = '/trash/'
        self.assertRaises(StopWordError, get_stop_words, 'german')
        stop_words.STOP_WORDS_DIR = original_stop_words_dir

    def test_safe_get_stop_words(self):
        self.assertRaises(StopWordError, get_stop_words, 'huttese')
        self.assertEqual(safe_get_stop_words('huttese'), [])


loader = TestLoader()

test_suite = TestSuite(
    [
        loader.loadTestsFromTestCase(StopWordsTestCase),
    ]
)
