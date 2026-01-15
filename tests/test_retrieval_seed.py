"""Tests for retrieval with seed data."""

import pytest
from phrasebot.config import default_config
from phrasebot.data import load_phrases
from phrasebot.retrieval import load_nlp, retrieve, build_phrase_cache
from phrasebot.models import MatchMode


@pytest.fixture(scope="module")
def nlp():
    """Load spaCy model once for all tests."""
    return load_nlp(default_config.spacy_model)


@pytest.fixture(scope="module")
def phrases():
    """Load phrases once for all tests."""
    return load_phrases(default_config)


@pytest.fixture(scope="module")
def phrase_cache(phrases, nlp):
    """Build phrase cache once for all tests."""
    return build_phrase_cache(phrases, nlp, default_config)


class TestSeedRetrieval:
    """Tests for retrieval on seed data."""

    def test_bathroom_query(self, nlp, phrases, phrase_cache):
        """Test that 'where is the bathroom' matches bathroom phrase."""
        result = retrieve(
            "where is the bathroom",
            phrases, nlp, default_config,
            phrase_cache=phrase_cache
        )
        assert result.best is not None
        assert "bathroom" in result.best.phrase.english.lower() or \
               "baño" in result.best.phrase.spanish.lower()

    def test_help_query(self, nlp, phrases, phrase_cache):
        """Test that 'help me' matches emergency help phrase."""
        result = retrieve(
            "help me",
            phrases, nlp, default_config,
            phrase_cache=phrase_cache
        )
        assert result.best is not None
        assert result.best.phrase.category in ["emergency", "essentials"]

    def test_taxi_query(self, nlp, phrases, phrase_cache):
        """Test that taxi query matches transportation phrase."""
        result = retrieve(
            "how much is a taxi",
            phrases, nlp, default_config,
            phrase_cache=phrase_cache
        )
        assert result.best is not None
        assert result.best.phrase.category == "transportation" or \
               "taxi" in result.best.phrase.english.lower()

    def test_restaurant_query(self, nlp, phrases, phrase_cache):
        """Test that restaurant query returns dining phrase."""
        result = retrieve(
            "I want to order food",
            phrases, nlp, default_config,
            phrase_cache=phrase_cache
        )
        assert result.best is not None

    def test_empty_query(self, nlp, phrases, phrase_cache):
        """Test that empty query doesn't crash."""
        result = retrieve(
            "",
            phrases, nlp, default_config,
            phrase_cache=phrase_cache
        )
        # Should return some result without crashing
        assert result is not None
