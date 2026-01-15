#!/usr/bin/env python3
"""
Evaluate retrieval accuracy on test dataset.

Computes:
- Top-1 accuracy: Best match equals expected
- Top-3 accuracy: Expected ID in top 3 candidates
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from phrasebot.config import default_config
from phrasebot.data import load_phrases, load_tests
from phrasebot.retrieval import load_nlp, retrieve, build_phrase_cache
from phrasebot.models import MatchMode


def evaluate(use_wordnet: bool = True, verbose: bool = False):
    """Run evaluation and return metrics."""
    print("Loading data...")
    phrases = load_phrases(default_config)
    tests = load_tests(default_config)
    print(f"  {len(phrases)} phrases, {len(tests)} test cases")

    print(f"Loading spaCy model ({default_config.spacy_model})...")
    nlp = load_nlp(default_config.spacy_model)

    print("Building phrase cache...")
    phrase_cache = build_phrase_cache(phrases, nlp, default_config)

    print()
    print("Running evaluation...")
    print("-" * 50)

    top1_correct = 0
    top3_correct = 0
    total = 0
    no_match_count = 0

    for i, test in enumerate(tests):
        if test.expected_id is None:
            # Skip no-match tests for accuracy calculation
            continue

        total += 1

        result = retrieve(
            query=test.query,
            phrases=phrases,
            nlp=nlp,
            config=default_config,
            use_wordnet=use_wordnet,
            phrase_cache=phrase_cache,
        )

        # Check top-1
        if result.best and result.best.phrase.id == test.expected_id:
            top1_correct += 1
            top1_hit = True
        else:
            top1_hit = False

        # Check top-3
        candidate_ids = [c.phrase.id for c in result.candidates]
        if test.expected_id in candidate_ids:
            top3_correct += 1
            top3_hit = True
        else:
            top3_hit = False

        if result.mode == MatchMode.NO_MATCH:
            no_match_count += 1

        # Verbose output for misses
        if verbose and not top1_hit:
            best_id = result.best.phrase.id if result.best else "None"
            best_score = result.best.score if result.best else 0
            print(f"  MISS: '{test.query}'")
            print(f"    Expected: {test.expected_id}")
            print(f"    Got: {best_id} (score: {best_score:.3f})")
            print()

    print()
    print("=" * 50)
    print("EVALUATION RESULTS")
    print("=" * 50)
    print()
    print(f"Total test cases: {total}")
    print(f"WordNet expansion: {'enabled' if use_wordnet else 'disabled'}")
    print()

    top1_acc = (top1_correct / total * 100) if total > 0 else 0
    top3_acc = (top3_correct / total * 100) if total > 0 else 0

    print(f"Top-1 Accuracy: {top1_correct}/{total} ({top1_acc:.1f}%)")
    print(f"Top-3 Accuracy: {top3_correct}/{total} ({top3_acc:.1f}%)")
    print(f"No-match responses: {no_match_count}")
    print()

    return {
        "top1_accuracy": top1_acc,
        "top3_accuracy": top3_acc,
        "top1_correct": top1_correct,
        "top3_correct": top3_correct,
        "total": total,
        "no_match_count": no_match_count,
    }


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Evaluate phrase retrieval accuracy")
    parser.add_argument("--no-wordnet", action="store_true",
                        help="Disable WordNet expansion")
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="Show details for missed queries")
    args = parser.parse_args()

    try:
        results = evaluate(
            use_wordnet=not args.no_wordnet,
            verbose=args.verbose
        )

        # Exit with success if accuracy is reasonable
        if results["top1_accuracy"] >= 50:
            print("Evaluation completed successfully!")
            sys.exit(0)
        else:
            print("Warning: Low accuracy - consider improving the dataset")
            sys.exit(0)  # Still exit 0, just warn

    except FileNotFoundError as e:
        print(f"Error: {e}")
        print("Run 'python scripts/generate_data.py' first.")
        sys.exit(1)
    except RuntimeError as e:
        print(f"Error: {e}")
        print("Run 'python scripts/setup_models.py' first.")
        sys.exit(1)


if __name__ == "__main__":
    main()
