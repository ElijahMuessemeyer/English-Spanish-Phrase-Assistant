"""
Data loading and saving utilities.
"""

import json
from pathlib import Path
from typing import Optional

from phrasebot.models import Phrase, TestCase
from phrasebot.config import Config, default_config


def load_phrases(config: Optional[Config] = None) -> list[Phrase]:
    """
    Load phrases from the data file.

    Falls back to seed file if main phrases.json doesn't exist.
    """
    if config is None:
        config = default_config

    # Try main file first, then seed file
    if config.phrases_path.exists():
        path = config.phrases_path
    elif config.phrases_seed_path.exists():
        path = config.phrases_seed_path
    else:
        raise FileNotFoundError(
            f"No phrase data found. Expected at {config.phrases_path} "
            f"or {config.phrases_seed_path}"
        )

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    return [Phrase.from_dict(item) for item in data]


def save_phrases(phrases: list[Phrase], path: Path) -> None:
    """Save phrases to a JSON file."""
    data = [phrase.to_dict() for phrase in phrases]

    # Ensure parent directory exists
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def load_tests(config: Optional[Config] = None) -> list[TestCase]:
    """
    Load test cases from the data file.

    Falls back to seed file if main tests.json doesn't exist.
    """
    if config is None:
        config = default_config

    # Try main file first, then seed file
    if config.tests_path.exists():
        path = config.tests_path
    elif config.tests_seed_path.exists():
        path = config.tests_seed_path
    else:
        raise FileNotFoundError(
            f"No test data found. Expected at {config.tests_path} "
            f"or {config.tests_seed_path}"
        )

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    return [TestCase.from_dict(item) for item in data]


def save_tests(tests: list[TestCase], path: Path) -> None:
    """Save test cases to a JSON file."""
    data = [test.to_dict() for test in tests]

    # Ensure parent directory exists
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def get_categories(phrases: list[Phrase]) -> list[str]:
    """Get unique categories from phrases."""
    return sorted(set(phrase.category for phrase in phrases))


def get_phrases_by_category(
    phrases: list[Phrase], category: str
) -> list[Phrase]:
    """Get all phrases in a specific category."""
    return [p for p in phrases if p.category == category]


def validate_phrases(phrases: list[Phrase]) -> list[str]:
    """
    Validate phrase data and return list of issues.

    Returns empty list if all valid.
    """
    issues = []
    ids_seen = set()

    for phrase in phrases:
        # Check for duplicate IDs
        if phrase.id in ids_seen:
            issues.append(f"Duplicate ID: {phrase.id}")
        ids_seen.add(phrase.id)

        # Check required fields
        if not phrase.english.strip():
            issues.append(f"Empty English text for {phrase.id}")
        if not phrase.spanish.strip():
            issues.append(f"Empty Spanish text for {phrase.id}")
        if not phrase.category.strip():
            issues.append(f"Empty category for {phrase.id}")

        # Check ID format (should be category_NNN)
        if "_" not in phrase.id:
            issues.append(f"Invalid ID format (expected category_NNN): {phrase.id}")

    return issues
