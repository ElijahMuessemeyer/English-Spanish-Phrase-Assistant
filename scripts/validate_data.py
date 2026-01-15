#!/usr/bin/env python3
"""
Validate phrase and test datasets.

Checks for:
- Schema compliance
- Duplicate IDs
- Missing required fields
- Orphan test references
"""

import json
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from phrasebot.config import default_config


REQUIRED_PHRASE_FIELDS = {"id", "english", "spanish", "category"}
VALID_CATEGORIES = {
    "essentials", "dining", "transportation", "directions",
    "hotel", "money", "shopping", "health", "emergency", "social"
}


def validate_phrases(phrases: list) -> list[str]:
    """Validate phrase data and return list of issues."""
    issues = []
    ids_seen = set()

    for i, phrase in enumerate(phrases):
        prefix = f"Phrase {i+1}"

        # Check required fields
        for field in REQUIRED_PHRASE_FIELDS:
            if field not in phrase:
                issues.append(f"{prefix}: Missing required field '{field}'")
            elif not str(phrase[field]).strip():
                issues.append(f"{prefix}: Empty field '{field}'")

        # Check ID format
        if "id" in phrase:
            pid = phrase["id"]
            if pid in ids_seen:
                issues.append(f"{prefix}: Duplicate ID '{pid}'")
            ids_seen.add(pid)

            if "_" not in pid:
                issues.append(f"{prefix}: Invalid ID format '{pid}' (expected category_NNN)")

        # Check category
        if "category" in phrase:
            cat = phrase["category"]
            if cat not in VALID_CATEGORIES:
                issues.append(f"{prefix}: Invalid category '{cat}'")

        # Check alts is a list
        if "alts" in phrase and not isinstance(phrase["alts"], list):
            issues.append(f"{prefix}: 'alts' must be a list")

    return issues


def validate_tests(tests: list, phrase_ids: set) -> list[str]:
    """Validate test data and return list of issues."""
    issues = []

    for i, test in enumerate(tests):
        prefix = f"Test {i+1}"

        # Check required fields
        if "query" not in test:
            issues.append(f"{prefix}: Missing 'query' field")
        elif not test["query"].strip():
            issues.append(f"{prefix}: Empty 'query'")

        # Check expected_id references valid phrase
        if "expected_id" in test and test["expected_id"]:
            eid = test["expected_id"]
            if eid not in phrase_ids:
                issues.append(f"{prefix}: Unknown expected_id '{eid}'")

    return issues


def main():
    print("Validating datasets...")
    print()

    all_issues = []

    # Load and validate phrases
    try:
        if default_config.phrases_path.exists():
            path = default_config.phrases_path
        else:
            path = default_config.phrases_seed_path

        print(f"Loading phrases from {path}...")
        with open(path, "r", encoding="utf-8") as f:
            phrases = json.load(f)

        print(f"  Found {len(phrases)} phrases")
        issues = validate_phrases(phrases)
        all_issues.extend(issues)

        phrase_ids = {p["id"] for p in phrases if "id" in p}
        print(f"  Unique IDs: {len(phrase_ids)}")

    except FileNotFoundError:
        print("  ERROR: No phrase file found!")
        all_issues.append("No phrase file found")
        phrases = []
        phrase_ids = set()

    print()

    # Load and validate tests
    try:
        if default_config.tests_path.exists():
            path = default_config.tests_path
        else:
            path = default_config.tests_seed_path

        print(f"Loading tests from {path}...")
        with open(path, "r", encoding="utf-8") as f:
            tests = json.load(f)

        print(f"  Found {len(tests)} test cases")
        issues = validate_tests(tests, phrase_ids)
        all_issues.extend(issues)

    except FileNotFoundError:
        print("  ERROR: No test file found!")
        all_issues.append("No test file found")

    print()

    # Report results
    if all_issues:
        print("=" * 50)
        print(f"VALIDATION FAILED: {len(all_issues)} issue(s) found")
        print("=" * 50)
        for issue in all_issues:
            print(f"  - {issue}")
        sys.exit(1)
    else:
        print("=" * 50)
        print("VALIDATION PASSED: No issues found!")
        print("=" * 50)
        sys.exit(0)


if __name__ == "__main__":
    main()
