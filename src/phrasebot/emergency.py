"""
Emergency phrase quick-access and prioritization.

Provides fast access to critical medical and safety phrases.
"""

from typing import Optional

from phrasebot.models import Phrase, Candidate


# Emergency detection keywords
EMERGENCY_KEYWORDS = {
    "help",
    "emergency",
    "police",
    "ambulance",
    "hospital",
    "doctor",
    "hurt",
    "injured",
    "sick",
    "pain",
    "danger",
    "dangerous",
    "unsafe",
    "attack",
    "attacked",
    "robbery",
    "robbed",
    "stolen",
    "thief",
    "lost",
    "passport",
    "fire",
    "accident",
    "allergic",
    "allergy",
    "medicine",
    "medication",
    "stop",
    "leave",
    "alone",
}

# Emergency command shortcuts
EMERGENCY_COMMANDS = {"/emergency", "!emergency", "emergency"}

# Emergency categories (prioritized in order)
EMERGENCY_CATEGORIES = ["emergency", "health"]


def is_emergency_query(text: str) -> bool:
    """
    Detect if a query is emergency-related.

    Checks for:
    - Emergency command shortcuts
    - Emergency keywords in text

    Args:
        text: User input text

    Returns:
        True if emergency-related
    """
    if not text:
        return False

    lower = text.lower().strip()

    # Check for command shortcuts
    if lower in EMERGENCY_COMMANDS:
        return True

    # Check for emergency keywords
    words = set(lower.split())
    if words & EMERGENCY_KEYWORDS:
        return True

    return False


def get_emergency_phrases(phrases: list[Phrase]) -> list[Phrase]:
    """
    Get all emergency-related phrases.

    Args:
        phrases: All available phrases

    Returns:
        List of emergency phrases sorted by category priority
    """
    emergency = []

    # Get phrases from emergency categories
    for category in EMERGENCY_CATEGORIES:
        for phrase in phrases:
            if phrase.category == category and phrase not in emergency:
                emergency.append(phrase)

    return emergency


def prioritize_emergency_candidates(
    candidates: list[Candidate],
) -> list[Candidate]:
    """
    Move emergency-category candidates to the top.

    Args:
        candidates: List of candidates from retrieval

    Returns:
        Reordered candidates with emergency phrases first
    """
    if not candidates:
        return candidates

    emergency = []
    other = []

    for candidate in candidates:
        if candidate.phrase.category in EMERGENCY_CATEGORIES:
            emergency.append(candidate)
        else:
            other.append(candidate)

    return emergency + other


def format_emergency_menu(phrases: list[Phrase]) -> str:
    """
    Format emergency phrases as a menu.

    Groups by sub-topic for easy scanning.

    Args:
        phrases: Emergency phrases

    Returns:
        Formatted menu string
    """
    if not phrases:
        return "No emergency phrases available."

    # Group by common topics
    topics = {
        "Getting Help": [],
        "Medical": [],
        "Police/Safety": [],
        "Lost Items": [],
        "Other": [],
    }

    for phrase in phrases:
        lower = phrase.english.lower()

        if any(w in lower for w in ["help", "need", "assistance"]):
            topics["Getting Help"].append(phrase)
        elif any(w in lower for w in ["hospital", "doctor", "sick", "hurt", "allerg", "medicine", "pain"]):
            topics["Medical"].append(phrase)
        elif any(w in lower for w in ["police", "thief", "stolen", "robbery", "danger", "unsafe", "stop", "leave"]):
            topics["Police/Safety"].append(phrase)
        elif any(w in lower for w in ["lost", "passport", "wallet", "missing"]):
            topics["Lost Items"].append(phrase)
        else:
            topics["Other"].append(phrase)

    # Build menu
    lines = []
    for topic, topic_phrases in topics.items():
        if not topic_phrases:
            continue

        lines.append(f"\n[{topic}]")
        for phrase in topic_phrases[:5]:  # Limit per topic
            lines.append(f"  {phrase.english}")
            lines.append(f"    -> {phrase.spanish}")
            if phrase.pronunciation:
                lines.append(f"       ({phrase.pronunciation})")

    return "\n".join(lines)


def emergency_shortcuts_help() -> str:
    """
    Get help text for emergency shortcuts.

    Returns:
        Help text string
    """
    return (
        "Emergency Quick Access:\n"
        "  Type /emergency or !emergency to see all emergency phrases\n"
        "  Or type keywords like 'help', 'police', 'hospital' for quick matches"
    )
