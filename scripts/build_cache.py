#!/usr/bin/env python3
"""
Build and cache phrase vectors for faster retrieval.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from phrasebot.config import default_config
from phrasebot.data import load_phrases
from phrasebot.retrieval import load_nlp, build_phrase_cache, save_cache


def main():
    print("Building phrase vector cache...")
    print()

    # Load phrases
    try:
        phrases = load_phrases(default_config)
        print(f"Loaded {len(phrases)} phrases")
    except FileNotFoundError as e:
        print(f"Error: {e}")
        print("Run 'python scripts/generate_data.py' first.")
        sys.exit(1)

    # Load spaCy model
    print(f"Loading spaCy model ({default_config.spacy_model})...")
    try:
        nlp = load_nlp(default_config.spacy_model)
    except RuntimeError as e:
        print(f"Error: {e}")
        sys.exit(1)

    # Build cache
    print("Computing phrase vectors...")
    cache = build_phrase_cache(phrases, nlp, default_config)
    print(f"Cached {len(cache)} phrase vectors")

    # Save cache
    print(f"Saving cache to {default_config.cache_path}...")
    save_cache(cache, default_config.cache_path)

    print()
    print("Cache built successfully!")


if __name__ == "__main__":
    main()
