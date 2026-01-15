"""
Command-line interface for the phrase assistant.
"""

import sys
from typing import Optional

from phrasebot.config import Config, default_config
from phrasebot.data import load_phrases, get_categories, get_phrases_by_category
from phrasebot.models import Phrase, RetrievalResult, MatchMode, Candidate
from phrasebot.retrieval import load_nlp, retrieve, load_cache, build_phrase_cache
from phrasebot.logging_utils import log_interaction

# Try to import rich for enhanced output
try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    from rich import print as rprint
    RICH_AVAILABLE = True
    console = Console()
except ImportError:
    RICH_AVAILABLE = False
    console = None


def print_welcome():
    """Print welcome message and instructions."""
    if RICH_AVAILABLE:
        console.print(Panel.fit(
            "[bold blue]English to Spanish Travel Phrase Assistant[/]\n\n"
            "Type what you want to say in English, and I'll find the best Spanish phrase.\n\n"
            "[dim]Commands:[/]\n"
            "  [green]exit[/] or [green]quit[/] - Exit the assistant\n"
            "  [green]help[/] - Show this help message\n"
            "  [green]categories[/] - List all phrase categories\n"
            "  [green]/emergency[/] - Quick access to emergency phrases",
            title="Welcome",
            border_style="blue",
        ))
    else:
        print("=" * 60)
        print("  English to Spanish Travel Phrase Assistant")
        print("=" * 60)
        print()
        print("Type what you want to say in English, and I'll find")
        print("the best Spanish phrase.")
        print()
        print("Commands:")
        print("  exit/quit  - Exit the assistant")
        print("  help       - Show this help message")
        print("  categories - List all phrase categories")
        print("  /emergency - Quick access to emergency phrases")
        print()


def print_phrase(phrase: Phrase, score: Optional[float] = None):
    """Print a phrase match."""
    if RICH_AVAILABLE:
        score_text = f" [dim](score: {score:.2f})[/]" if score else ""
        console.print(Panel(
            f"[bold green]{phrase.spanish}[/]\n\n"
            f"[yellow]Pronunciation:[/] {phrase.pronunciation}\n"
            f"[blue]Category:[/] {phrase.category}{score_text}",
            title=f"[white]{phrase.english}[/]",
            border_style="green",
        ))
    else:
        print()
        print(f"  English: {phrase.english}")
        print(f"  Spanish: {phrase.spanish}")
        print(f"  Pronunciation: {phrase.pronunciation}")
        print(f"  Category: {phrase.category}")
        if score:
            print(f"  (Match score: {score:.2f})")
        print()


def print_candidates(candidates: list[Candidate]):
    """Print candidate matches for user selection."""
    if RICH_AVAILABLE:
        table = Table(title="Multiple matches found - please select one:")
        table.add_column("#", style="cyan", width=3)
        table.add_column("English", style="white")
        table.add_column("Spanish", style="green")
        table.add_column("Score", style="dim", width=6)

        for i, candidate in enumerate(candidates, 1):
            table.add_row(
                str(i),
                candidate.phrase.english,
                candidate.phrase.spanish,
                f"{candidate.score:.2f}",
            )
        console.print(table)
    else:
        print()
        print("Multiple matches found - please select one:")
        print()
        for i, candidate in enumerate(candidates, 1):
            print(f"  {i}. {candidate.phrase.english}")
            print(f"     Spanish: {candidate.phrase.spanish}")
            print(f"     (Score: {candidate.score:.2f})")
            print()


def print_no_match(categories: list[str]):
    """Print no match message with suggestions."""
    if RICH_AVAILABLE:
        cats = ", ".join(categories[:5])
        console.print(Panel(
            "[yellow]I couldn't find a good match for that phrase.[/]\n\n"
            "Try rephrasing or be more specific.\n\n"
            f"[dim]Available categories: {cats}...[/]\n"
            "[dim]Type 'categories' to see all categories.[/]",
            title="No Match",
            border_style="yellow",
        ))
    else:
        print()
        print("I couldn't find a good match for that phrase.")
        print("Try rephrasing or be more specific.")
        print()
        print(f"Available categories: {', '.join(categories[:5])}...")
        print("Type 'categories' to see all categories.")
        print()


def print_categories(categories: list[str]):
    """Print available categories."""
    if RICH_AVAILABLE:
        cats = "\n".join(f"  - {cat}" for cat in categories)
        console.print(Panel(
            f"[white]{cats}[/]",
            title="Available Categories",
            border_style="blue",
        ))
    else:
        print()
        print("Available categories:")
        for cat in categories:
            print(f"  - {cat}")
        print()


def get_user_selection(max_choice: int) -> Optional[int]:
    """Get user's selection from candidates."""
    while True:
        try:
            if RICH_AVAILABLE:
                console.print("[cyan]Enter number (or 0 to skip):[/] ", end="")
            else:
                print("Enter number (or 0 to skip): ", end="")

            choice = input().strip()

            if not choice:
                return None

            num = int(choice)
            if num == 0:
                return None
            if 1 <= num <= max_choice:
                return num - 1  # Convert to 0-indexed

            print(f"Please enter a number between 1 and {max_choice}, or 0 to skip.")
        except ValueError:
            print("Please enter a valid number.")
        except (EOFError, KeyboardInterrupt):
            return None


def handle_emergency(phrases: list[Phrase]):
    """Handle emergency quick-access command."""
    try:
        from phrasebot.emergency import get_emergency_phrases, format_emergency_menu
        emergency_phrases = get_emergency_phrases(phrases)
        menu = format_emergency_menu(emergency_phrases)

        if RICH_AVAILABLE:
            console.print(Panel(menu, title="[red]Emergency Phrases[/]", border_style="red"))
        else:
            print()
            print("=" * 40)
            print("  EMERGENCY PHRASES")
            print("=" * 40)
            print(menu)
            print()
    except ImportError:
        # Emergency module not yet implemented
        emergency = get_phrases_by_category(phrases, "emergency")
        print()
        print("Emergency phrases:")
        for p in emergency[:5]:
            print(f"  - {p.english}")
            print(f"    {p.spanish}")
        print()


def run_cli(config: Optional[Config] = None):
    """
    Run the interactive CLI chat loop.

    Args:
        config: Configuration (uses default if None)
    """
    if config is None:
        config = default_config

    # Load data
    try:
        phrases = load_phrases(config)
    except FileNotFoundError as e:
        print(f"Error: {e}")
        print("Run 'python scripts/generate_data.py' first.")
        sys.exit(1)

    categories = get_categories(phrases)

    # Load spaCy model
    print("Loading language model...")
    try:
        nlp = load_nlp(config.spacy_model)
    except RuntimeError as e:
        print(f"Error: {e}")
        print("Run 'python scripts/setup_models.py' first.")
        sys.exit(1)

    # Try to load cache
    phrase_cache = load_cache(config.cache_path)
    if phrase_cache is None:
        print("Building phrase cache (this may take a moment)...")
        phrase_cache = build_phrase_cache(phrases, nlp, config)

    print_welcome()

    # Main loop
    while True:
        try:
            if RICH_AVAILABLE:
                console.print("[bold cyan]You:[/] ", end="")
            else:
                print("You: ", end="")

            user_input = input().strip()

            if not user_input:
                continue

            # Handle commands
            lower_input = user_input.lower()

            if lower_input in ("exit", "quit", "q"):
                print("Goodbye! Safe travels!")
                break

            if lower_input == "help":
                print_welcome()
                continue

            if lower_input == "categories":
                print_categories(categories)
                continue

            if lower_input in ("/emergency", "!emergency", "emergency"):
                handle_emergency(phrases)
                continue

            # Retrieve matching phrase
            result = retrieve(
                query=user_input,
                phrases=phrases,
                nlp=nlp,
                config=config,
                use_wordnet=True,
                phrase_cache=phrase_cache,
            )

            # Handle result based on mode
            user_selection = None

            if result.mode == MatchMode.MATCH:
                print_phrase(result.best.phrase, result.best.score)

            elif result.mode == MatchMode.CANDIDATES:
                print_candidates(result.candidates)
                selection = get_user_selection(len(result.candidates))
                if selection is not None:
                    selected = result.candidates[selection]
                    user_selection = selected.phrase.id
                    print_phrase(selected.phrase, selected.score)

            else:  # NO_MATCH
                print_no_match(categories)

            # Log interaction
            log_interaction(user_input, result, user_selection, config)

        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye! Safe travels!")
            break


def main():
    """Main entry point."""
    run_cli()


if __name__ == "__main__":
    main()
