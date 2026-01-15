"""Smoke tests for evaluation script."""

import pytest
import subprocess
import sys
from pathlib import Path


class TestEvalSmoke:
    """Smoke tests to ensure eval script runs."""

    def test_eval_imports(self):
        """Test that eval module can be imported."""
        # This tests that all dependencies are available
        scripts_dir = Path(__file__).parent.parent / "scripts"
        sys.path.insert(0, str(scripts_dir.parent / "src"))

        # Should not raise ImportError
        from phrasebot.config import default_config
        from phrasebot.data import load_phrases, load_tests
        from phrasebot.retrieval import load_nlp

    def test_data_can_be_loaded(self):
        """Test that phrase data can be loaded."""
        from phrasebot.data import load_phrases, load_tests
        from phrasebot.config import default_config

        # Should load without error (uses seed if generated not available)
        phrases = load_phrases(default_config)
        assert len(phrases) > 0

    def test_retrieval_works(self):
        """Test that retrieval returns results."""
        from phrasebot.data import load_phrases
        from phrasebot.retrieval import load_nlp, retrieve
        from phrasebot.config import default_config

        phrases = load_phrases(default_config)
        nlp = load_nlp(default_config.spacy_model)

        result = retrieve("bathroom", phrases, nlp, default_config)
        assert result is not None

    def test_cli_module_imports(self):
        """Test that CLI module can be imported."""
        from phrasebot.cli import run_cli, main
        # Should not raise ImportError
        assert callable(run_cli)
        assert callable(main)
