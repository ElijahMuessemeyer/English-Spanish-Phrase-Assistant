"""
Text preprocessing pipeline for the phrase assistant.

Includes normalization, spelling correction, and lemmatization.
"""

import re
import string
from typing import Optional

# Lazy imports to handle missing dependencies gracefully
_nltk_available = None
_textblob_available = None
_lemmatizer = None
_stopwords = None


def _check_nltk():
    """Check if NLTK is available and initialize resources."""
    global _nltk_available, _lemmatizer, _stopwords

    if _nltk_available is not None:
        return _nltk_available

    try:
        import nltk
        from nltk.stem import WordNetLemmatizer
        from nltk.corpus import stopwords

        _lemmatizer = WordNetLemmatizer()
        try:
            _stopwords = set(stopwords.words("english"))
        except LookupError:
            _stopwords = set()

        _nltk_available = True
    except ImportError:
        _nltk_available = False

    return _nltk_available


def _check_textblob():
    """Check if TextBlob is available."""
    global _textblob_available

    if _textblob_available is not None:
        return _textblob_available

    try:
        from textblob import TextBlob
        _textblob_available = True
    except ImportError:
        _textblob_available = False

    return _textblob_available


def normalize_text(text: str) -> str:
    """
    Normalize text by lowercasing, trimming whitespace,
    and handling punctuation safely.

    Args:
        text: Raw input text

    Returns:
        Normalized text
    """
    if not text:
        return ""

    # Lowercase
    text = text.lower()

    # Replace common contractions
    contractions = {
        "i'm": "i am",
        "i've": "i have",
        "i'll": "i will",
        "i'd": "i would",
        "you're": "you are",
        "you've": "you have",
        "you'll": "you will",
        "you'd": "you would",
        "he's": "he is",
        "she's": "she is",
        "it's": "it is",
        "we're": "we are",
        "we've": "we have",
        "we'll": "we will",
        "they're": "they are",
        "they've": "they have",
        "they'll": "they will",
        "that's": "that is",
        "what's": "what is",
        "where's": "where is",
        "who's": "who is",
        "how's": "how is",
        "there's": "there is",
        "here's": "here is",
        "let's": "let us",
        "can't": "cannot",
        "won't": "will not",
        "don't": "do not",
        "doesn't": "does not",
        "didn't": "did not",
        "isn't": "is not",
        "aren't": "are not",
        "wasn't": "was not",
        "weren't": "were not",
        "haven't": "have not",
        "hasn't": "has not",
        "hadn't": "had not",
        "couldn't": "could not",
        "wouldn't": "would not",
        "shouldn't": "should not",
        "mustn't": "must not",
        "needn't": "need not",
    }

    for contraction, expansion in contractions.items():
        text = text.replace(contraction, expansion)

    # Remove punctuation except for essential marks
    # Keep: letters, numbers, spaces
    text = re.sub(r"[^\w\s]", " ", text)

    # Normalize whitespace
    text = " ".join(text.split())

    return text.strip()


def correct_spelling(text: str) -> str:
    """
    Apply spelling correction using TextBlob.

    Fails gracefully if TextBlob is unavailable.

    Args:
        text: Input text

    Returns:
        Corrected text (or original if correction fails)
    """
    if not text:
        return ""

    if not _check_textblob():
        return text

    try:
        from textblob import TextBlob
        blob = TextBlob(text)
        corrected = str(blob.correct())
        return corrected
    except Exception:
        # Fail gracefully - return original text
        return text


def tokenize(text: str) -> list[str]:
    """
    Tokenize text into words.

    Args:
        text: Input text

    Returns:
        List of tokens
    """
    if not text:
        return []

    if _check_nltk():
        try:
            import nltk
            return nltk.word_tokenize(text)
        except Exception:
            pass

    # Fallback: simple split
    return text.split()


def lemmatize(text: str) -> str:
    """
    Lemmatize text using NLTK WordNet lemmatizer.

    Args:
        text: Input text

    Returns:
        Lemmatized text
    """
    if not text:
        return ""

    if not _check_nltk():
        return text

    try:
        tokens = tokenize(text)
        lemmatized = [_lemmatizer.lemmatize(token) for token in tokens]
        return " ".join(lemmatized)
    except Exception:
        # Fail gracefully
        return text


def remove_stopwords(text: str) -> str:
    """
    Remove common English stopwords.

    Args:
        text: Input text

    Returns:
        Text with stopwords removed
    """
    if not text:
        return ""

    if not _check_nltk() or not _stopwords:
        return text

    tokens = tokenize(text)
    filtered = [t for t in tokens if t.lower() not in _stopwords]
    return " ".join(filtered)


def preprocess(
    text: str,
    spell_correct: bool = True,
    remove_stops: bool = False
) -> str:
    """
    Full preprocessing pipeline.

    Pipeline order:
    1. Normalize (lowercase, expand contractions, clean punctuation)
    2. Spell correct (optional, TextBlob)
    3. Lemmatize (NLTK WordNet)
    4. Remove stopwords (optional)

    Args:
        text: Raw input text
        spell_correct: Whether to apply spelling correction
        remove_stops: Whether to remove stopwords

    Returns:
        Preprocessed text
    """
    if not text:
        return ""

    # Step 1: Normalize
    result = normalize_text(text)

    # Step 2: Spell correct (optional)
    if spell_correct:
        result = correct_spelling(result)

    # Step 3: Lemmatize
    result = lemmatize(result)

    # Step 4: Remove stopwords (optional)
    if remove_stops:
        result = remove_stopwords(result)

    return result


def get_tokens(text: str) -> list[str]:
    """
    Get preprocessed tokens from text.

    Args:
        text: Raw input text

    Returns:
        List of preprocessed tokens
    """
    preprocessed = preprocess(text, spell_correct=False, remove_stops=False)
    return tokenize(preprocessed)
