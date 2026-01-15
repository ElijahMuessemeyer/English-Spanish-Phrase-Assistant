"""
WordNet-based query expansion with guardrails.

Expands user queries with synonyms to improve retrieval recall.
"""

from typing import Optional

# Lazy imports
_wordnet_available = None
_wordnet = None
_stopwords = None


def _check_wordnet():
    """Check if WordNet is available and initialize."""
    global _wordnet_available, _wordnet, _stopwords

    if _wordnet_available is not None:
        return _wordnet_available

    try:
        from nltk.corpus import wordnet, stopwords

        # Test that WordNet data is available
        wordnet.synsets("test")

        _wordnet = wordnet
        try:
            _stopwords = set(stopwords.words("english"))
        except LookupError:
            _stopwords = set()

        _wordnet_available = True
    except (ImportError, LookupError):
        _wordnet_available = False

    return _wordnet_available


def get_pos_tag(word: str) -> Optional[str]:
    """
    Get simple POS tag for a word (for WordNet lookup).

    Returns 'n' for nouns, 'v' for verbs, None otherwise.
    We only expand nouns and verbs to avoid overreach.
    """
    try:
        import nltk
        # Simple heuristic based on common word endings
        # This avoids needing the full POS tagger for simple cases
        if word.endswith(('ing', 'ed', 'es', 's')) and len(word) > 4:
            return 'v'
        if word.endswith(('tion', 'ness', 'ment', 'ity')):
            return 'n'
        # Default to noun for content words
        return 'n'
    except ImportError:
        return 'n'


def get_synonyms(
    word: str,
    pos: Optional[str] = None,
    max_synonyms: int = 2,
) -> list[str]:
    """
    Get synonyms for a word from WordNet.

    Args:
        word: Word to find synonyms for
        pos: Part of speech ('n' for noun, 'v' for verb)
        max_synonyms: Maximum number of synonyms to return

    Returns:
        List of synonym strings (may be empty)
    """
    if not _check_wordnet():
        return []

    try:
        synsets = _wordnet.synsets(word, pos=pos) if pos else _wordnet.synsets(word)

        synonyms = set()
        for synset in synsets[:3]:  # Limit synsets to check
            for lemma in synset.lemmas():
                name = lemma.name().lower()
                # Skip multi-word expressions and the original word
                if "_" not in name and name != word.lower():
                    synonyms.add(name)

                if len(synonyms) >= max_synonyms:
                    break
            if len(synonyms) >= max_synonyms:
                break

        return list(synonyms)[:max_synonyms]
    except Exception:
        return []


def expand_query_with_wordnet(
    tokens: list[str],
    max_synonyms_per_token: int = 2,
    max_total_tokens: int = 30,
) -> list[str]:
    """
    Expand query tokens with WordNet synonyms.

    Guardrails:
    - Only expand nouns and verbs (simple heuristic)
    - Exclude stopwords
    - Cap synonyms per token
    - Cap total tokens after expansion
    - Prefer single-word synonyms (no underscores)
    - Return original tokens if WordNet unavailable

    Args:
        tokens: List of tokens from preprocessed query
        max_synonyms_per_token: Max synonyms to add per token
        max_total_tokens: Max total tokens after expansion

    Returns:
        Expanded list of tokens (includes originals)
    """
    if not tokens:
        return []

    if not _check_wordnet():
        return tokens

    # Start with original tokens
    expanded = list(tokens)

    for token in tokens:
        # Skip stopwords
        if _stopwords and token.lower() in _stopwords:
            continue

        # Skip very short tokens
        if len(token) < 3:
            continue

        # Get POS for targeted expansion
        pos = get_pos_tag(token)

        # Only expand nouns and verbs
        if pos not in ('n', 'v'):
            continue

        # Get synonyms
        synonyms = get_synonyms(token, pos, max_synonyms_per_token)

        # Add synonyms to expanded list
        for syn in synonyms:
            if syn not in expanded:
                expanded.append(syn)

            # Check total token limit
            if len(expanded) >= max_total_tokens:
                return expanded

    return expanded


def expand_query_string(
    query: str,
    max_synonyms_per_token: int = 2,
    max_total_tokens: int = 30,
) -> str:
    """
    Expand a query string with WordNet synonyms.

    Convenience function that tokenizes, expands, and rejoins.

    Args:
        query: Query string
        max_synonyms_per_token: Max synonyms per token
        max_total_tokens: Max total tokens

    Returns:
        Expanded query string
    """
    tokens = query.lower().split()
    expanded = expand_query_with_wordnet(tokens, max_synonyms_per_token, max_total_tokens)
    return " ".join(expanded)
