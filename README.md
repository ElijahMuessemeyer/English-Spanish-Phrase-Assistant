# English to Spanish Travel Phrase Assistant

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![spaCy](https://img.shields.io/badge/spaCy-3.5+-09a3d5.svg)](https://spacy.io/)

A retrieval-based, closed-domain CLI chatbot that helps English-speaking travelers find the best Spanish phrase for common travel situations.

## Overview

This project implements a **retrieval-based chatbot** (not generative) that matches user queries to a curated database of Spanish travel phrases using **semantic similarity**. The system uses NLP techniques to understand user intent even when phrasing differs from exact database entries.

### Key Features

- **Semantic Matching**: Uses spaCy word vectors to find the best phrase match based on meaning, not just keywords
- **Fuzzy Input Handling**: Handles typos, informal phrasing, and indirect queries
- **WordNet Query Expansion**: Enhances queries with synonyms to improve recall
- **Emergency Quick-Access**: Priority handling for medical and safety situations
- **Pronunciation Guides**: Each phrase includes phonetic pronunciation
- **Interactive CLI**: User-friendly chat interface with candidate selection

## Quick Start

### 1. Install Dependencies

```bash
# Create and activate virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install the package
pip install -e .
pip install -e ".[dev]"  # Include dev dependencies for testing
```

### 2. Download NLP Models

```bash
python scripts/setup_models.py
```

This downloads:
- spaCy English model with word vectors (`en_core_web_md`)
- NLTK resources (punkt, wordnet, stopwords)
- TextBlob corpora

### 3. Generate Phrase Database

```bash
python scripts/generate_data.py
python scripts/validate_data.py
python scripts/build_cache.py
```

### 4. Run the Assistant

```bash
python -m phrasebot
```

## Usage

Once running, simply type what you want to say in English:

```
You: Where is the bathroom?

┌─ Where is the bathroom? ─────────────────────────┐
│ ¿Dónde está el baño?                             │
│                                                   │
│ Pronunciation: DOHN-deh es-TAH el BAN-yoh        │
│ Category: essentials                              │
└───────────────────────────────────────────────────┘

You: I need help!

┌─ I need help. ───────────────────────────────────┐
│ Necesito ayuda.                                   │
│                                                   │
│ Pronunciation: neh-seh-SEE-toh ah-YOO-dah        │
│ Category: emergency                               │
└───────────────────────────────────────────────────┘
```

### Commands

| Command | Description |
|---------|-------------|
| `exit` or `quit` | Exit the assistant |
| `help` | Show help message |
| `categories` | List all phrase categories |
| `/emergency` | Quick access to emergency phrases |

### Match Modes

The assistant responds differently based on match confidence:

1. **Confident Match** (score >= 0.72): Returns single best phrase directly
2. **Multiple Candidates** (score >= 0.55): Shows top 3 options for selection
3. **No Match** (score < 0.55): Suggests rephrasing and shows categories

## Technical Details

### Architecture

- **Type**: Retrieval-based (selects from database, doesn't generate)
- **Domain**: Closed-domain (travel situations only)
- **Interface**: Command-line interface (CLI)

### NLP Pipeline

1. **Preprocessing**:
   - Text normalization (lowercase, whitespace)
   - Contraction expansion ("where's" → "where is")
   - Spelling correction (TextBlob)
   - Lemmatization (NLTK WordNet)

2. **Query Expansion** (optional):
   - WordNet synonym expansion
   - Guardrails to prevent over-expansion

3. **Similarity Matching**:
   - spaCy `en_core_web_md` word vectors (300 dimensions)
   - Cosine similarity comparison
   - Threshold-based result modes

### Libraries Used

| Library | Purpose |
|---------|---------|
| spaCy | Word vectors and similarity matching |
| NLTK | Tokenization, lemmatization, WordNet |
| TextBlob | Spelling correction |
| Rich | Enhanced CLI output (optional) |

### Phrase Categories

- **essentials**: Basic greetings, questions, common phrases
- **dining**: Restaurant, food, allergies
- **transportation**: Taxi, bus, train, airport
- **directions**: Navigation, locations
- **hotel**: Check-in, amenities, issues
- **money**: Currency, payments, ATM
- **shopping**: Stores, prices, returns
- **health**: Medical, pharmacy, symptoms
- **emergency**: Police, accidents, urgent help
- **social**: Conversations, pleasantries

## Evaluation

Run the evaluation script to measure accuracy:

```bash
python scripts/eval.py
```

Metrics:
- **Top-1 Accuracy**: Best match equals expected result
- **Top-3 Accuracy**: Expected result in top 3 candidates

## Testing

```bash
# Run all tests
pytest -q

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_preprocess.py
```

## Project Structure

```
phrase-assistant/
├── README.md
├── pyproject.toml
├── data/
│   ├── phrases.json          # Generated phrase database
│   ├── tests.json            # Generated test cases
│   ├── phrases.seed.json     # Seed data for development
│   ├── tests.seed.json       # Seed test cases
│   ├── cache.pkl             # Cached phrase vectors
│   └── logs.jsonl            # Interaction logs
├── scripts/
│   ├── setup_models.py       # Download NLP models
│   ├── generate_data.py      # Generate phrase database
│   ├── validate_data.py      # Validate data integrity
│   ├── build_cache.py        # Build vector cache
│   └── eval.py               # Evaluate accuracy
├── src/phrasebot/
│   ├── __init__.py
│   ├── __main__.py           # Entry point
│   ├── config.py             # Configuration
│   ├── models.py             # Data models
│   ├── data.py               # Data loading
│   ├── preprocess.py         # Text preprocessing
│   ├── wordnet_expand.py     # Query expansion
│   ├── retrieval.py          # Similarity matching
│   ├── emergency.py          # Emergency handling
│   ├── logging_utils.py      # Interaction logging
│   └── cli.py                # CLI interface
└── tests/
    ├── test_preprocess.py
    ├── test_retrieval_seed.py
    ├── test_thresholds.py
    ├── test_wordnet_expand.py
    ├── test_emergency.py
    └── test_eval_smoke.py
```

## Configuration

Key configuration values in `src/phrasebot/config.py`:

```python
confident_threshold = 0.72   # Minimum score for confident match
candidate_threshold = 0.55   # Minimum score for candidate list
max_candidates = 3           # Maximum candidates to show
spacy_model = "en_core_web_md"
```

## How It Works

1. **User Input**: User types an English phrase (e.g., "I lost my passport")

2. **Preprocessing**:
   - Normalizes text
   - Corrects spelling errors
   - Lemmatizes words

3. **Query Expansion**:
   - Adds WordNet synonyms (e.g., "lost" → "misplace")
   - Guards against over-expansion

4. **Similarity Search**:
   - Converts query to vector using spaCy
   - Compares against all phrase vectors
   - Ranks by cosine similarity

5. **Response Selection**:
   - High confidence → Return single match
   - Medium confidence → Show top 3 for selection
   - Low confidence → Suggest rephrasing

6. **Display Result**:
   - Spanish translation
   - Phonetic pronunciation
   - Category label

## License

This project was created as an academic portfolio project.

## Acknowledgments

- spaCy for excellent NLP tools
- NLTK for linguistic resources
- Course materials from CSU Global
