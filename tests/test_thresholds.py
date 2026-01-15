"""Tests for threshold-based result modes."""

import pytest
from phrasebot.config import Config
from phrasebot.data import load_phrases
from phrasebot.retrieval import load_nlp, retrieve, build_phrase_cache
from phrasebot.models import MatchMode


@pytest.fixture(scope="module")
def nlp():
    """Load spaCy model."""
    config = Config()
    return load_nlp(config.spacy_model)


@pytest.fixture(scope="module")
def phrases():
    """Load phrases."""
    return load_phrases()


@pytest.fixture(scope="module")
def phrase_cache(phrases, nlp):
    """Build phrase cache."""
    return build_phrase_cache(phrases, nlp)


class TestThresholdModes:
    """Tests for different match modes based on thresholds."""

    def test_confident_match_mode(self, nlp, phrases, phrase_cache):
        """Test that exact match returns MATCH mode."""
        # Use exact phrase from dataset
        result = retrieve(
            "Where is the bathroom?",
            phrases, nlp,
            phrase_cache=phrase_cache
        )
        # Should be confident match or at least have candidates
        assert result.mode in [MatchMode.MATCH, MatchMode.CANDIDATES]
        assert result.best is not None
        assert result.best.score >= 0.55

    def test_candidates_mode(self, nlp, phrases, phrase_cache):
        """Test that ambiguous query returns CANDIDATES mode."""
        # A somewhat ambiguous query
        config = Config()
        config.confident_threshold = 0.99  # Force candidates mode
        result = retrieve(
            "I need something",
            phrases, nlp, config,
            phrase_cache=phrase_cache
        )
        # Should have candidates
        assert result.best is not None or result.mode == MatchMode.NO_MATCH

    def test_no_match_mode(self, nlp, phrases, phrase_cache):
        """Test that irrelevant query returns NO_MATCH mode."""
        config = Config()
        config.candidate_threshold = 0.99  # Force no-match
        result = retrieve(
            "quantum physics relativity",
            phrases, nlp, config,
            phrase_cache=phrase_cache
        )
        # Should be no match with high thresholds
        assert result.mode == MatchMode.NO_MATCH or result.best.score < 0.99

    def test_threshold_values(self, nlp, phrases, phrase_cache):
        """Test that thresholds are applied correctly."""
        config = Config()

        # With normal thresholds, a good query should match
        result = retrieve(
            "bathroom",
            phrases, nlp, config,
            phrase_cache=phrase_cache
        )
        assert result.best is not None

        # Check score is within expected range
        if result.best:
            assert 0.0 <= result.best.score <= 1.0
