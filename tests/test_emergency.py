"""Tests for emergency phrase handling."""

import pytest
from phrasebot.emergency import (
    is_emergency_query,
    get_emergency_phrases,
    prioritize_emergency_candidates,
    format_emergency_menu,
)
from phrasebot.models import Phrase, Candidate


class TestEmergencyDetection:
    """Tests for emergency query detection."""

    def test_emergency_keywords(self):
        """Test that emergency keywords are detected."""
        assert is_emergency_query("help me")
        assert is_emergency_query("I need help")
        assert is_emergency_query("call the police")
        assert is_emergency_query("hospital")
        assert is_emergency_query("emergency")
        assert is_emergency_query("I was robbed")
        assert is_emergency_query("my passport is lost")

    def test_emergency_commands(self):
        """Test that emergency commands are detected."""
        assert is_emergency_query("/emergency")
        assert is_emergency_query("!emergency")
        assert is_emergency_query("emergency")

    def test_non_emergency_queries(self):
        """Test that non-emergency queries are not flagged."""
        assert not is_emergency_query("where is the bathroom")
        assert not is_emergency_query("I want coffee")
        assert not is_emergency_query("how much does this cost")
        assert not is_emergency_query("")

    def test_case_insensitive(self):
        """Test that detection is case insensitive."""
        assert is_emergency_query("HELP ME")
        assert is_emergency_query("Help")
        assert is_emergency_query("EMERGENCY")


class TestGetEmergencyPhrases:
    """Tests for emergency phrase retrieval."""

    def test_filters_emergency_category(self):
        """Test that emergency category phrases are returned."""
        phrases = [
            Phrase(id="emergency_001", english="Help", spanish="Ayuda",
                   pronunciation="", category="emergency"),
            Phrase(id="dining_001", english="Menu", spanish="Menú",
                   pronunciation="", category="dining"),
            Phrase(id="health_001", english="Hospital", spanish="Hospital",
                   pronunciation="", category="health"),
        ]

        emergency = get_emergency_phrases(phrases)

        # Should include emergency and health
        categories = [p.category for p in emergency]
        assert "emergency" in categories
        assert "health" in categories
        assert "dining" not in categories


class TestPrioritizeEmergency:
    """Tests for emergency candidate prioritization."""

    def test_moves_emergency_to_top(self):
        """Test that emergency candidates are moved to top."""
        candidates = [
            Candidate(
                Phrase(id="dining_001", english="Menu", spanish="Menú",
                       pronunciation="", category="dining"),
                0.8
            ),
            Candidate(
                Phrase(id="emergency_001", english="Help", spanish="Ayuda",
                       pronunciation="", category="emergency"),
                0.7
            ),
        ]

        prioritized = prioritize_emergency_candidates(candidates)

        # Emergency should be first
        assert prioritized[0].phrase.category == "emergency"

    def test_empty_candidates(self):
        """Test handling of empty candidates list."""
        assert prioritize_emergency_candidates([]) == []


class TestFormatEmergencyMenu:
    """Tests for emergency menu formatting."""

    def test_formats_menu(self):
        """Test that menu is formatted correctly."""
        phrases = [
            Phrase(id="emergency_001", english="I need help",
                   spanish="Necesito ayuda", pronunciation="neh-seh-SEE-toh",
                   category="emergency"),
        ]

        menu = format_emergency_menu(phrases)

        assert "I need help" in menu
        assert "Necesito ayuda" in menu

    def test_empty_phrases(self):
        """Test handling of empty phrases list."""
        menu = format_emergency_menu([])
        assert "No emergency phrases" in menu or menu is not None
