"""
Logging utilities for the phrase assistant.

Writes JSONL logs with fail-safe handling (never crashes the app).
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Optional

from phrasebot.models import LogEntry, RetrievalResult, MatchMode
from phrasebot.config import Config, default_config


def create_log_entry(
    query: str,
    result: RetrievalResult,
    user_selection: Optional[str] = None,
) -> LogEntry:
    """
    Create a log entry from a query and result.

    Args:
        query: Original user query
        result: Retrieval result
        user_selection: ID of phrase selected by user (for candidates mode)

    Returns:
        LogEntry object
    """
    result_id = None
    score = None
    candidates = []

    if result.best:
        result_id = result.best.phrase.id
        score = result.best.score

    if result.candidates:
        candidates = [c.phrase.id for c in result.candidates]

    return LogEntry(
        timestamp=datetime.now().isoformat(),
        query=query,
        normalized_query=result.normalized_query,
        mode=result.mode.value,
        result_id=result_id,
        score=score,
        candidates=candidates,
        user_selection=user_selection,
    )


def append_log(
    entry: LogEntry,
    config: Optional[Config] = None,
) -> bool:
    """
    Append a log entry to the JSONL log file.

    Fails gracefully and never raises exceptions.

    Args:
        entry: LogEntry to append
        config: Configuration (uses default if None)

    Returns:
        True if logged successfully, False otherwise
    """
    if config is None:
        config = default_config

    try:
        # Ensure directory exists
        config.log_path.parent.mkdir(parents=True, exist_ok=True)

        # Append to log file
        with open(config.log_path, "a", encoding="utf-8") as f:
            json.dump(entry.to_dict(), f, ensure_ascii=False)
            f.write("\n")

        return True
    except Exception:
        # Fail gracefully - logging should never crash the app
        return False


def log_interaction(
    query: str,
    result: RetrievalResult,
    user_selection: Optional[str] = None,
    config: Optional[Config] = None,
) -> bool:
    """
    Log a user interaction.

    Convenience function that creates and appends a log entry.

    Args:
        query: Original user query
        result: Retrieval result
        user_selection: ID of phrase selected by user
        config: Configuration

    Returns:
        True if logged successfully, False otherwise
    """
    entry = create_log_entry(query, result, user_selection)
    return append_log(entry, config)


def read_logs(config: Optional[Config] = None) -> list[LogEntry]:
    """
    Read all log entries from the log file.

    Args:
        config: Configuration

    Returns:
        List of LogEntry objects
    """
    if config is None:
        config = default_config

    if not config.log_path.exists():
        return []

    entries = []
    try:
        with open(config.log_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    data = json.loads(line)
                    entries.append(LogEntry(**data))
    except Exception:
        pass

    return entries


def clear_logs(config: Optional[Config] = None) -> bool:
    """
    Clear the log file.

    Args:
        config: Configuration

    Returns:
        True if cleared successfully, False otherwise
    """
    if config is None:
        config = default_config

    try:
        if config.log_path.exists():
            config.log_path.unlink()
        return True
    except Exception:
        return False
