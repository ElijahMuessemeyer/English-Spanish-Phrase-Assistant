#!/usr/bin/env python3
"""
Setup script to download required NLP models and resources.
Run this before using the phrase assistant.
"""

import subprocess
import sys


def download_spacy_model():
    """Download spaCy English model with word vectors."""
    print("Downloading spaCy model (en_core_web_md)...")
    try:
        subprocess.run(
            [sys.executable, "-m", "spacy", "download", "en_core_web_md"],
            check=True
        )
        print("spaCy model downloaded successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error downloading spaCy model: {e}")
        sys.exit(1)


def download_nltk_resources():
    """Download required NLTK resources."""
    print("Downloading NLTK resources...")
    import nltk

    resources = [
        ('punkt', 'tokenizers/punkt'),
        ('punkt_tab', 'tokenizers/punkt_tab'),
        ('wordnet', 'corpora/wordnet'),
        ('omw-1.4', 'corpora/omw-1.4'),
        ('averaged_perceptron_tagger', 'taggers/averaged_perceptron_tagger'),
        ('stopwords', 'corpora/stopwords'),
    ]

    for name, path in resources:
        try:
            nltk.data.find(path)
            print(f"  {name}: already installed")
        except LookupError:
            print(f"  {name}: downloading...")
            nltk.download(name, quiet=True)
            print(f"  {name}: installed")

    print("NLTK resources downloaded successfully.")


def download_textblob_corpora():
    """Download TextBlob corpora for spelling correction."""
    print("Downloading TextBlob corpora...")
    try:
        subprocess.run(
            [sys.executable, "-m", "textblob.download_corpora", "lite"],
            check=True,
            capture_output=True
        )
        print("TextBlob corpora downloaded successfully.")
    except subprocess.CalledProcessError:
        print("TextBlob corpora download skipped (may already exist).")


def main():
    print("=" * 60)
    print("English to Spanish Travel Phrase Assistant - Setup")
    print("=" * 60)
    print()

    download_spacy_model()
    print()
    download_nltk_resources()
    print()
    download_textblob_corpora()

    print()
    print("=" * 60)
    print("Setup complete! You can now run the phrase assistant.")
    print("=" * 60)


if __name__ == "__main__":
    main()
