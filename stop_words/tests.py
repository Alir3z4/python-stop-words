"""
Tests for stop-words
"""
import random
from unittest import TestCase
from unittest import TestSuite
from unittest import TestLoader

import stop_words
from stop_words import get_stop_words
from stop_words import safe_get_stop_words
from stop_words import StopWordError
from stop_words import LANGUAGE_MAPPING
from stop_words import AVAILABLE_LANGUAGES


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
        self.assertFalse('french' in stop_words.STOP_WORDS_CACHE)
        sw = get_stop_words('fr')
        self.assertTrue('french' in stop_words.STOP_WORDS_CACHE)
        original_stop_words_dir = stop_words.STOP_WORDS_DIR
        stop_words.STOP_WORDS_DIR = 'not-existing-directory'
        self.assertEqual(sw, get_stop_words('french'))
        stop_words.STOP_WORDS_DIR = original_stop_words_dir
        try:
            get_stop_words('klingon')
        except:
            pass
        self.assertFalse('klingon' in stop_words.STOP_WORDS_CACHE)

    def test_get_stop_words_unavailable_language(self):
        self.assertRaises(StopWordError, get_stop_words, 'sindarin')

    def test_get_stop_words_install_issue(self):
        original_stop_words_dir = stop_words.STOP_WORDS_DIR
        stop_words.STOP_WORDS_DIR = 'not-existing-directory'
        self.assertRaises(StopWordError, get_stop_words, 'german')
        stop_words.STOP_WORDS_DIR = original_stop_words_dir

    def test_safe_get_stop_words(self):
        self.assertRaises(StopWordError, get_stop_words, 'huttese')
        self.assertEqual(safe_get_stop_words('huttese'), [])

    def test_random_language_stop_words_load(self):
        languages = list(LANGUAGE_MAPPING.keys()) + list(AVAILABLE_LANGUAGES)
        sample = random.sample(languages, len(languages))
        for language in sample:
            stop_words = safe_get_stop_words(language)
            self.assertTrue(
                len(stop_words) > 0,
                'Cannot load stopwords for {0} language'.format(language)
            )

    def test_filters(self):
            language = 'en'
            before = get_stop_words(language, False)
            letter = random.choice(random.choice(before))

            def remove_letter(stopwords, language):
                return [word for word in stopwords if letter not in word]
            stop_words.add_filter(remove_letter)
            after = get_stop_words(language, False)
            for stopword in after:
                self.assertFalse(letter in stopword)
            self.assertTrue(stop_words.remove_filter(remove_letter))


loader = TestLoader()

test_suite = TestSuite(
    [
        loader.loadTestsFromTestCase(StopWordsTestCase),
    ]
)
