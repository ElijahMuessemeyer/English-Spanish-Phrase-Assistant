"""
Data models for the phrase assistant.
"""

from dataclasses import dataclass, field
from typing import Optional
from enum import Enum


@dataclass
class Phrase:
    """A travel phrase with translations and metadata."""

    id: str
    english: str
    spanish: str
    pronunciation: str
    category: str
    alts: list[str] = field(default_factory=list)

    def get_searchable_text(self) -> str:
        """Get combined English text for similarity matching."""
        texts = [self.english] + self.alts
        return " | ".join(texts)

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "id": self.id,
            "english": self.english,
            "spanish": self.spanish,
            "pronunciation": self.pronunciation,
            "category": self.category,
            "alts": self.alts,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Phrase":
        """Create a Phrase from a dictionary."""
        return cls(
            id=data["id"],
            english=data["english"],
            spanish=data["spanish"],
            pronunciation=data.get("pronunciation", ""),
            category=data["category"],
            alts=data.get("alts", []),
        )


@dataclass
class Candidate:
    """A phrase match candidate with similarity score."""

    phrase: Phrase
    score: float

    def __lt__(self, other: "Candidate") -> bool:
        """Sort by score descending."""
        return self.score > other.score


class MatchMode(Enum):
    """Result mode based on similarity thresholds."""

    MATCH = "match"  # Confident single match (score >= 0.72)
    CANDIDATES = "candidates"  # Multiple candidates (score >= 0.55)
    NO_MATCH = "no_match"  # No good matches (score < 0.55)


@dataclass
class RetrievalResult:
    """Result of a retrieval query."""

    mode: MatchMode
    best: Optional[Candidate] = None
    candidates: list[Candidate] = field(default_factory=list)
    normalized_query: str = ""

    @property
    def has_match(self) -> bool:
        """Check if there's a confident match."""
        return self.mode == MatchMode.MATCH and self.best is not None

    @property
    def has_candidates(self) -> bool:
        """Check if there are candidate matches."""
        return self.mode == MatchMode.CANDIDATES and len(self.candidates) > 0


@dataclass
class TestCase:
    """A test case for evaluation."""

    query: str
    expected_id: Optional[str]

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "query": self.query,
            "expected_id": self.expected_id,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "TestCase":
        """Create a TestCase from a dictionary."""
        return cls(
            query=data["query"],
            expected_id=data.get("expected_id"),
        )


@dataclass
class LogEntry:
    """A log entry for an interaction."""

    timestamp: str
    query: str
    normalized_query: str
    mode: str
    result_id: Optional[str]
    score: Optional[float]
    candidates: list[str] = field(default_factory=list)
    user_selection: Optional[str] = None

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "timestamp": self.timestamp,
            "query": self.query,
            "normalized_query": self.normalized_query,
            "mode": self.mode,
            "result_id": self.result_id,
            "score": self.score,
            "candidates": self.candidates,
            "user_selection": self.user_selection,
        }
