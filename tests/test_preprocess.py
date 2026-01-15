"""Tests for preprocessing module."""

import pytest
from phrasebot.preprocess import normalize_text, preprocess, tokenize


class TestNormalizeText:
    """Tests for text normalization."""

    def test_lowercase(self):
        assert normalize_text("HELLO") == "hello"
        assert normalize_text("Hello World") == "hello world"

    def test_whitespace(self):
        assert normalize_text("  hello  ") == "hello"
        assert normalize_text("hello   world") == "hello world"

    def test_contractions(self):
        assert "where is" in normalize_text("where's")
        assert "i am" in normalize_text("I'm")
        assert "do not" in normalize_text("don't")
        assert "cannot" in normalize_text("can't")

    def test_punctuation(self):
        assert normalize_text("Hello!") == "hello"
        assert normalize_text("What?") == "what"
        assert normalize_text("Hello, world.") == "hello world"

    def test_empty_input(self):
        assert normalize_text("") == ""
        assert normalize_text(None) == "" or normalize_text(None) is None

    def test_mixed_input(self):
        result = normalize_text("  Where's the BATHROOM?  ")
        assert "where" in result
        assert "bathroom" in result


class TestPreprocess:
    """Tests for full preprocessing pipeline."""

    def test_basic_preprocessing(self):
        result = preprocess("Where is the bathroom?", spell_correct=False)
        assert "bathroom" in result.lower()

    def test_handles_weird_input(self):
        # Should not crash on weird input
        assert preprocess("") == ""
        assert preprocess("???") is not None
        assert preprocess("123") is not None
        assert preprocess("a" * 1000) is not None


class TestTokenize:
    """Tests for tokenization."""

    def test_basic_tokenize(self):
        tokens = tokenize("hello world")
        assert len(tokens) >= 2
        assert "hello" in tokens
        assert "world" in tokens

    def test_empty_tokenize(self):
        assert tokenize("") == []
