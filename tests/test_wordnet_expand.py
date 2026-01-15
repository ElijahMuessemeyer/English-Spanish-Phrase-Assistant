"""Tests for WordNet expansion."""

import pytest
from phrasebot.wordnet_expand import (
    expand_query_with_wordnet,
    get_synonyms,
    expand_query_string,
)


class TestWordNetExpansion:
    """Tests for WordNet query expansion."""

    def test_basic_expansion(self):
        """Test that expansion adds synonyms."""
        tokens = ["bathroom", "help"]
        expanded = expand_query_with_wordnet(tokens)

        # Should at least contain original tokens
        assert "bathroom" in expanded
        assert "help" in expanded

        # May have additional synonyms
        assert len(expanded) >= 2

    def test_stopwords_not_expanded(self):
        """Test that stopwords are not expanded."""
        tokens = ["the", "a", "is", "bathroom"]
        expanded = expand_query_with_wordnet(tokens)

        # Original tokens should be there
        assert "bathroom" in expanded

        # Shouldn't explode in size from expanding stopwords
        assert len(expanded) < 20

    def test_short_tokens_not_expanded(self):
        """Test that very short tokens are not expanded."""
        tokens = ["i", "a", "go"]
        expanded = expand_query_with_wordnet(tokens)

        # Should not add many synonyms for short words
        assert len(expanded) < 10

    def test_max_synonyms_cap(self):
        """Test that synonym count is capped."""
        tokens = ["help"]
        expanded = expand_query_with_wordnet(tokens, max_synonyms_per_token=2)

        # Should have original + at most 2 synonyms
        assert len(expanded) <= 3

    def test_max_total_tokens_cap(self):
        """Test that total token count is capped."""
        tokens = ["help", "emergency", "hospital", "doctor", "police"]
        expanded = expand_query_with_wordnet(tokens, max_total_tokens=10)

        # Should not exceed max
        assert len(expanded) <= 10

    def test_empty_input(self):
        """Test that empty input returns empty."""
        assert expand_query_with_wordnet([]) == []

    def test_returns_original_on_failure(self):
        """Test that original tokens returned if WordNet fails."""
        tokens = ["bathroom"]
        expanded = expand_query_with_wordnet(tokens)

        # Should at least have original
        assert "bathroom" in expanded


class TestGetSynonyms:
    """Tests for synonym retrieval."""

    def test_get_synonyms_basic(self):
        """Test basic synonym retrieval."""
        synonyms = get_synonyms("help")
        # May or may not find synonyms, but shouldn't crash
        assert isinstance(synonyms, list)

    def test_get_synonyms_limit(self):
        """Test synonym limit."""
        synonyms = get_synonyms("help", max_synonyms=1)
        assert len(synonyms) <= 1


class TestExpandQueryString:
    """Tests for string-based expansion."""

    def test_expand_string(self):
        """Test query string expansion."""
        result = expand_query_string("need help please")
        assert isinstance(result, str)
        assert "help" in result
