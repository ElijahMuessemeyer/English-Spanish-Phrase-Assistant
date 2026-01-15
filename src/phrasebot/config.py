"""
Configuration settings for the phrase assistant.
"""

from pathlib import Path
from dataclasses import dataclass


@dataclass
class Config:
    """Application configuration."""

    # Similarity thresholds
    confident_threshold: float = 0.72
    candidate_threshold: float = 0.55
    max_candidates: int = 3

    # spaCy model
    spacy_model: str = "en_core_web_md"

    # Paths (relative to project root)
    data_dir: Path = None
    phrases_path: Path = None
    phrases_seed_path: Path = None
    tests_path: Path = None
    tests_seed_path: Path = None
    cache_path: Path = None
    log_path: Path = None

    def __post_init__(self):
        """Set up paths relative to package location."""
        if self.data_dir is None:
            # Find the data directory relative to the package
            package_dir = Path(__file__).parent.parent.parent
            self.data_dir = package_dir / "data"

        if self.phrases_path is None:
            self.phrases_path = self.data_dir / "phrases.json"
        if self.phrases_seed_path is None:
            self.phrases_seed_path = self.data_dir / "phrases.seed.json"
        if self.tests_path is None:
            self.tests_path = self.data_dir / "tests.json"
        if self.tests_seed_path is None:
            self.tests_seed_path = self.data_dir / "tests.seed.json"
        if self.cache_path is None:
            self.cache_path = self.data_dir / "cache.pkl"
        if self.log_path is None:
            self.log_path = self.data_dir / "logs.jsonl"


# Default configuration instance
default_config = Config()
