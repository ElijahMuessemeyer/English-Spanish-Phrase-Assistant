"""
Retrieval engine using spaCy semantic similarity.
"""

from typing import Optional
import pickle
from pathlib import Path

from phrasebot.models import Phrase, Candidate, MatchMode, RetrievalResult
from phrasebot.config import Config, default_config
from phrasebot.preprocess import preprocess

# Lazy spaCy loading
_nlp = None
_nlp_model_name = None


def load_nlp(model_name: str = "en_core_web_md"):
    """
    Load spaCy model (cached).

    Args:
        model_name: Name of spaCy model to load

    Returns:
        spaCy Language object
    """
    global _nlp, _nlp_model_name

    if _nlp is not None and _nlp_model_name == model_name:
        return _nlp

    try:
        import spacy
        _nlp = spacy.load(model_name)
        _nlp_model_name = model_name
        return _nlp
    except OSError:
        raise RuntimeError(
            f"spaCy model '{model_name}' not found. "
            f"Run: python -m spacy download {model_name}"
        )


def build_phrase_text(phrase: Phrase) -> str:
    """
    Build searchable text from a phrase.

    Combines English canonical text with alternatives.

    Args:
        phrase: Phrase object

    Returns:
        Combined text for similarity matching
    """
    texts = [phrase.english] + phrase.alts
    return " | ".join(texts)


def compute_similarity(query_doc, phrase_doc) -> float:
    """
    Compute cosine similarity between two spaCy docs.

    Args:
        query_doc: spaCy doc for user query
        phrase_doc: spaCy doc for phrase

    Returns:
        Similarity score (0.0 to 1.0)
    """
    if not query_doc.has_vector or not phrase_doc.has_vector:
        return 0.0

    return query_doc.similarity(phrase_doc)


def retrieve(
    query: str,
    phrases: list[Phrase],
    nlp=None,
    config: Optional[Config] = None,
    use_wordnet: bool = False,
    phrase_cache: Optional[dict] = None,
) -> RetrievalResult:
    """
    Retrieve best matching phrase(s) for a query.

    Pipeline:
    1. Preprocess query
    2. (Optional) WordNet expansion
    3. Compute similarity against all phrases
    4. Apply thresholds to determine result mode

    Args:
        query: User's input query
        phrases: List of Phrase objects to search
        nlp: spaCy Language object (loaded if None)
        config: Configuration (uses default if None)
        use_wordnet: Whether to apply WordNet expansion
        phrase_cache: Optional dict of phrase_id -> spaCy doc

    Returns:
        RetrievalResult with mode, best match, and candidates
    """
    if config is None:
        config = default_config

    if nlp is None:
        nlp = load_nlp(config.spacy_model)

    # Preprocess query
    normalized = preprocess(query, spell_correct=True, remove_stops=False)

    # Optional WordNet expansion
    if use_wordnet:
        try:
            from phrasebot.wordnet_expand import expand_query_with_wordnet
            from phrasebot.preprocess import get_tokens
            tokens = get_tokens(normalized)
            expanded_tokens = expand_query_with_wordnet(tokens)
            normalized = " ".join(expanded_tokens)
        except ImportError:
            pass

    # Create query document
    query_doc = nlp(normalized)

    # Compute similarities for all phrases
    candidates = []
    for phrase in phrases:
        # Use cached doc if available
        if phrase_cache and phrase.id in phrase_cache:
            phrase_doc = phrase_cache[phrase.id]
        else:
            phrase_text = build_phrase_text(phrase)
            phrase_doc = nlp(preprocess(phrase_text, spell_correct=False))

        score = compute_similarity(query_doc, phrase_doc)
        candidates.append(Candidate(phrase=phrase, score=score))

    # Sort by score (descending)
    candidates.sort()

    # Apply thresholds
    if not candidates:
        return RetrievalResult(
            mode=MatchMode.NO_MATCH,
            normalized_query=normalized,
        )

    best = candidates[0]

    if best.score >= config.confident_threshold:
        # Confident match
        return RetrievalResult(
            mode=MatchMode.MATCH,
            best=best,
            candidates=[best],
            normalized_query=normalized,
        )
    elif best.score >= config.candidate_threshold:
        # Multiple candidates
        top_candidates = candidates[: config.max_candidates]
        return RetrievalResult(
            mode=MatchMode.CANDIDATES,
            best=best,
            candidates=top_candidates,
            normalized_query=normalized,
        )
    else:
        # No match
        return RetrievalResult(
            mode=MatchMode.NO_MATCH,
            best=best,
            normalized_query=normalized,
        )


def build_phrase_cache(
    phrases: list[Phrase],
    nlp=None,
    config: Optional[Config] = None,
) -> dict:
    """
    Build a cache of phrase documents for faster retrieval.

    Args:
        phrases: List of Phrase objects
        nlp: spaCy Language object
        config: Configuration

    Returns:
        Dict mapping phrase_id to spaCy doc
    """
    if config is None:
        config = default_config

    if nlp is None:
        nlp = load_nlp(config.spacy_model)

    cache = {}
    for phrase in phrases:
        phrase_text = build_phrase_text(phrase)
        processed = preprocess(phrase_text, spell_correct=False)
        cache[phrase.id] = nlp(processed)

    return cache


def save_cache(cache: dict, path: Path) -> None:
    """Save phrase cache to disk."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "wb") as f:
        pickle.dump(cache, f)


def load_cache(path: Path) -> Optional[dict]:
    """Load phrase cache from disk."""
    if not path.exists():
        return None

    try:
        with open(path, "rb") as f:
            return pickle.load(f)
    except Exception:
        return None
