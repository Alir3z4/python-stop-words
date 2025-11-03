import random
from pathlib import Path
from unittest import TestCase

import stop_words
from stop_words import (
    AVAILABLE_LANGUAGES,
    LANGUAGE_MAPPING,
    STOP_WORDS_CACHE,
    StopWordError,
    add_filter,
    get_stop_words,
    get_version,
    remove_filter,
    safe_get_stop_words,
)


class TestStopWordsBasic(TestCase):
    """Test basic stop word loading functionality."""

    NUMBER_OF_ENGLISH_STOP_WORDS = 1333

    def test_get_stop_words_returns_list(self) -> None:
        """Stop words should be returned as a list."""
        sw = get_stop_words("english")
        self.assertIsInstance(sw, list)
        self.assertEqual(len(sw), self.NUMBER_OF_ENGLISH_STOP_WORDS)

    def test_get_stop_words_contains_strings(self) -> None:
        """All stop words should be strings."""
        sw = get_stop_words("english")
        self.assertTrue(all(isinstance(word, str) for word in sw))

    def test_get_stop_words_no_empty_strings(self) -> None:
        """Stop words should not contain empty strings."""
        sw = get_stop_words("english")
        self.assertTrue(all(word.strip() for word in sw))

    def test_get_stop_words_language_mapping(self) -> None:
        """Language codes should map to full language names."""
        sw_code = get_stop_words("en")
        sw_full = get_stop_words("english")
        self.assertEqual(len(sw_code), self.NUMBER_OF_ENGLISH_STOP_WORDS)
        self.assertEqual(sw_code, sw_full)

    def test_common_english_stop_words(self) -> None:
        """Common English stop words should be present."""
        sw = get_stop_words("en")
        common_words = ["the", "a", "an", "and", "or", "but", "is", "are"]
        for word in common_words:
            self.assertIn(word, sw, f"Expected '{word}' in English stop words")

    def test_get_version(self) -> None:
        self.assertIsNotNone(get_version())


class TestStopWordsCache(TestCase):
    """Test caching behavior."""

    def setUp(self) -> None:
        """Clear cache before each test."""
        STOP_WORDS_CACHE.clear()

    def test_cache_enabled_by_default(self) -> None:
        """Cache should be enabled by default."""
        self.assertNotIn("french", STOP_WORDS_CACHE)
        get_stop_words("fr")
        self.assertIn("french", STOP_WORDS_CACHE)

    def test_cache_disabled(self) -> None:
        """Cache should not be used when cache=False."""
        self.assertNotIn("german", STOP_WORDS_CACHE)
        get_stop_words("de", cache=False)
        self.assertNotIn("german", STOP_WORDS_CACHE)

    def test_cache_persists_across_calls(self) -> None:
        """Cached stop words should persist across calls."""
        original_dir = stop_words.STOP_WORDS_DIR

        # Load and cache
        sw1 = get_stop_words("fr")
        self.assertIn("french", STOP_WORDS_CACHE)

        # Break the file system path
        stop_words.STOP_WORDS_DIR = Path("non-existent-directory")

        # Should still work from cache
        sw2 = get_stop_words("french")
        self.assertEqual(sw1, sw2)

        # Restore
        stop_words.STOP_WORDS_DIR = original_dir

    def test_cache_miss_raises_error(self) -> None:
        """Cache miss with invalid path should raise error."""
        original_dir = stop_words.STOP_WORDS_DIR
        stop_words.STOP_WORDS_DIR = Path("non-existent-directory")

        with self.assertRaises(StopWordError):
            get_stop_words("spanish")

        self.assertNotIn("spanish", STOP_WORDS_CACHE)
        stop_words.STOP_WORDS_DIR = original_dir

    def test_returns_copy_not_reference(self) -> None:
        """get_stop_words should return a copy, not the cached reference."""
        sw1 = get_stop_words("en")
        sw2 = get_stop_words("en")

        # Modify one list
        sw1.append("custom_word")

        # The other should be unchanged
        self.assertNotIn("custom_word", sw2)

        # Cache should also be unchanged
        sw3 = get_stop_words("en")
        self.assertNotIn("custom_word", sw3)


class TestStopWordsErrors(TestCase):
    """Test error handling."""

    def test_unavailable_language_raises_error(self) -> None:
        """Unknown languages should raise StopWordError."""
        with self.assertRaises(StopWordError) as ctx:
            get_stop_words("sindarin")
        self.assertIn("sindarin", str(ctx.exception).lower())

    def test_missing_file_raises_error(self) -> None:
        """Missing language files should raise StopWordError."""
        original_dir = stop_words.STOP_WORDS_DIR
        stop_words.STOP_WORDS_DIR = Path("non-existent-directory")

        with self.assertRaises(StopWordError) as ctx:
            get_stop_words("german", cache=False)

        self.assertIn("unreadable", str(ctx.exception).lower())
        stop_words.STOP_WORDS_DIR = original_dir

    def test_safe_get_stop_words_no_exception(self) -> None:
        """safe_get_stop_words should never raise exceptions."""
        result = safe_get_stop_words("klingon")
        self.assertEqual(result, [])
        self.assertIsInstance(result, list)

    def test_safe_get_stop_words_with_valid_language(self) -> None:
        """safe_get_stop_words should work with valid languages."""
        result = safe_get_stop_words("en")
        self.assertGreater(len(result), 0)

    def test_error_message_includes_available_languages(self) -> None:
        """Error message should hint at available languages."""
        with self.assertRaises(StopWordError) as ctx:
            get_stop_words("notreal")
        error_msg = str(ctx.exception).lower()
        self.assertIn("available", error_msg)


class TestStopWordsFilters(TestCase):
    """Test the filter system."""

    def setUp(self) -> None:
        """Clear cache and filters before each test."""
        STOP_WORDS_CACHE.clear()
        stop_words._filters.clear()
        stop_words._filters[None] = []

    def tearDown(self) -> None:
        """Clean up filters after each test."""
        stop_words._filters.clear()
        stop_words._filters[None] = []

    def test_global_filter_removes_words(self) -> None:
        """Global filters should modify all languages."""

        def remove_short_words(words: list[str], _lang: str | None = None) -> list[str]:
            return [w for w in words if len(w) > 3]

        add_filter(remove_short_words)
        sw = get_stop_words("en", cache=False)

        self.assertTrue(all(len(word) > 3 for word in sw))

    def test_language_specific_filter(self) -> None:
        """Language-specific filters should only affect that language."""

        def uppercase_filter(words: list[str], _language: str | None = None) -> list[str]:
            return [w.upper() for w in words]

        add_filter(uppercase_filter, language="english")

        # English should be uppercase
        en_words = get_stop_words("en", cache=False)
        self.assertTrue(all(w.isupper() for w in en_words if not w.isnumeric()))

        # Other languages should be unaffected
        fr_words = get_stop_words("fr", cache=False)
        self.assertFalse(all(w.isupper() for w in fr_words))

    def test_multiple_filters_chain(self) -> None:
        """Multiple filters should be applied in sequence."""

        def add_prefix(words: list[str], _lang: str | None = None) -> list[str]:
            return [f"prefix_{w}" for w in words]

        def add_suffix(words: list[str], _lang: str | None = None) -> list[str]:
            return [f"{w}_suffix" for w in words]

        add_filter(add_prefix)
        add_filter(add_suffix)

        sw = get_stop_words("en", cache=False)
        sample_word = sw[0]

        self.assertTrue(sample_word.startswith("prefix_"))
        self.assertTrue(sample_word.endswith("_suffix"))

    def test_remove_filter_returns_true(self) -> None:
        """Removing an existing filter should return True."""

        def dummy_filter(words: list[str], _lang: str | None = None) -> list[str]:
            return words

        add_filter(dummy_filter)

        # Calling it to get the `dummy_filter` actually execute.
        get_stop_words("en")

        result = remove_filter(dummy_filter)
        self.assertTrue(result)

    def test_remove_nonexistent_filter_returns_false(self) -> None:
        """Removing a non-existent filter should return False."""

        def dummy_filter(words: list[str], _lang: str | None = None) -> list[str]:
            return words  # pragma: no cover

        result = remove_filter(dummy_filter)
        self.assertFalse(result)

    def test_remove_filter_with_language(self) -> None:
        """Language-specific filter removal should work."""

        def lang_filter(words: list[str], _language: str | None = None) -> list[str]:
            return words

        add_filter(lang_filter, language="english")

        # Calling it to get the `lang_filter` actually execute.
        get_stop_words("en")

        result = remove_filter(lang_filter, language="english")
        self.assertTrue(result)

        # Should return False when trying to remove again
        result = remove_filter(lang_filter, language="english")
        self.assertFalse(result)

    def test_filter_with_random_letter_removal(self) -> None:
        """Original test: remove words containing a random letter."""
        language = "en"
        before = get_stop_words(language, cache=False)
        letter = random.choice(random.choice(before))

        def remove_letter(words: list[str], _lang: str | None = None) -> list[str]:
            return [w for w in words if letter not in w]

        add_filter(remove_letter)
        after = get_stop_words(language, cache=False)

        for word in after:
            self.assertNotIn(letter, word)

        self.assertTrue(remove_filter(remove_letter))


class TestStopWordsAllLanguages(TestCase):
    """Test all available languages."""

    def test_all_mapped_languages_loadable(self) -> None:
        """All languages in LANGUAGE_MAPPING should be loadable."""
        for code, full_name in LANGUAGE_MAPPING.items():
            with self.subTest(code=code, language=full_name):
                sw = safe_get_stop_words(code)
                self.assertGreater(len(sw), 0, f"No stop words loaded for {full_name} ({code})")

    def test_random_language_loading(self) -> None:
        """Random sample of languages should all load successfully."""
        all_languages = list(LANGUAGE_MAPPING.keys()) + AVAILABLE_LANGUAGES
        sample = random.sample(all_languages, min(10, len(all_languages)))

        for language in sample:
            with self.subTest(language=language):
                sw = safe_get_stop_words(language)
                self.assertGreater(len(sw), 0, f"Cannot load stopwords for {language}")

    def test_all_languages_have_unique_words(self) -> None:
        """Each language should have at least some unique characteristics."""
        # Compare English and French as they should be different
        en = set(get_stop_words("en"))
        fr = set(get_stop_words("fr"))

        # Should have different words
        self.assertNotEqual(en, fr)
        # Should have some overlap (common borrowed words)
        self.assertGreater(len(en & fr), 0)


class TestStopWordsEdgeCases(TestCase):
    """Test edge cases and boundary conditions."""

    def test_empty_language_string(self) -> None:
        """Empty language string should raise error."""
        with self.assertRaises(StopWordError):
            get_stop_words("")

    def test_none_language(self) -> None:
        """None as language should raise appropriate error."""
        with self.assertRaises((StopWordError, KeyError, TypeError)):
            get_stop_words(None)  # type: ignore

    def test_case_sensitive_language_codes(self) -> None:
        """Language codes should be case-sensitive."""
        # Lowercase should work
        sw_lower = get_stop_words("en")
        self.assertGreater(len(sw_lower), 0)

        # Uppercase might not be in mapping
        with self.assertRaises(StopWordError):
            get_stop_words("EN")

    def test_whitespace_in_stop_words(self) -> None:
        """Stop words should be properly stripped of whitespace."""
        sw = get_stop_words("en")
        for word in sw:
            self.assertEqual(word, word.strip(), f"Word '{word}' has extra whitespace")

    def test_duplicate_stop_words(self) -> None:
        """Stop words list should not contain duplicates."""
        sw = get_stop_words("en")
        unique_words = set(sw)
        self.assertEqual(len(sw), len(unique_words), "Stop words list contains duplicates")

    def test_filter_returns_empty_list(self) -> None:
        """Filter that returns empty list should work."""

        def remove_all(words: list[str], _lang: str | None = None) -> list[str]:
            return []

        STOP_WORDS_CACHE.clear()
        stop_words._filters.clear()
        stop_words._filters[None] = []

        add_filter(remove_all)
        sw = get_stop_words("en", cache=False)
        self.assertEqual(sw, [])

        # Cleanup
        remove_filter(remove_all)

    def test_filter_adds_words(self) -> None:
        """Filter that adds words should work."""

        def add_custom(words: list[str], _lang: str | None = None) -> list[str]:
            return words + ["custom1", "custom2"]

        STOP_WORDS_CACHE.clear()
        stop_words._filters.clear()
        stop_words._filters[None] = []

        add_filter(add_custom)
        sw = get_stop_words("en", cache=False)

        self.assertIn("custom1", sw)
        self.assertIn("custom2", sw)

        # Cleanup
        remove_filter(add_custom)

    def test_concurrent_filter_modifications(self) -> None:
        """Adding and removing filters should be safe."""
        filters = [
            lambda w, language: w,
            lambda w, language: [word.upper() for word in w],
            lambda w, language: [word.lower() for word in w],
        ]

        STOP_WORDS_CACHE.clear()
        stop_words._filters.clear()
        stop_words._filters[None] = []

        # Add all filters
        for f in filters:
            add_filter(f)

        # Remove them in different order
        for f in reversed(filters):
            remove_filter(f)

        # Should be back to empty
        self.assertEqual(len(stop_words._filters[None]), 0)


class TestStopWordsConfiguration(TestCase):
    """Test module configuration and constants."""

    def test_available_languages_is_list(self) -> None:
        """AVAILABLE_LANGUAGES should be a list."""
        self.assertIsInstance(AVAILABLE_LANGUAGES, list)
        self.assertGreater(len(AVAILABLE_LANGUAGES), 0)

    def test_language_mapping_is_dict(self) -> None:
        """LANGUAGE_MAPPING should be a dictionary."""
        self.assertIsInstance(LANGUAGE_MAPPING, dict)
        self.assertGreater(len(LANGUAGE_MAPPING), 0)

    def test_cache_is_dict(self) -> None:
        """STOP_WORDS_CACHE should be a dictionary."""
        self.assertIsInstance(STOP_WORDS_CACHE, dict)

    def test_stop_words_dir_exists(self) -> None:
        """STOP_WORDS_DIR should point to an existing directory."""
        self.assertTrue(
            stop_words.STOP_WORDS_DIR.exists(),
            f"Stop words directory not found: {stop_words.STOP_WORDS_DIR}",
        )
        self.assertTrue(stop_words.STOP_WORDS_DIR.is_dir())

    def test_language_files_exist(self) -> None:
        """Language files referenced in mapping should exist."""
        for lang_name in AVAILABLE_LANGUAGES:
            lang_file = stop_words.STOP_WORDS_DIR / f"{lang_name}.txt"
            self.assertTrue(lang_file.exists(), f"Language file missing: {lang_file}")
