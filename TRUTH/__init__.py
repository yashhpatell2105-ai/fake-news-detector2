"""
TRUTH - Fake News Detection System
Main Package Entry Point

This package provides an AI-powered system to detect and combat
misinformation and fake news in digital media.

Theme: TRUTH - Uncovering facts in an information-rich world

Quick Start:
    1. pip install -r requirements.txt
    2. python demo.py
    3. python -m flask --app api.app run
    4. Visit http://localhost:5000

Project Structure:
    - src/          Core system modules (NLP, ML, verification)
    - api/          Flask REST API server
    - frontend/     Web interface (HTML/CSS/JS)
    - data/         Sample data for testing
    - demo.py       Feature demonstration script
    - test_system.py Component validation tests

Documentation:
    - README.md     Complete documentation
    - QUICKSTART.md 5-minute setup guide
    - TRUTH_SUMMARY.md Project overview

Features:
    ✓ Natural Language Processing
    ✓ Machine Learning fake news detection
    ✓ Source credibility verification
    ✓ Real-time fact-checking
    ✓ Web interface and REST API
    ✓ Comprehensive accuracy metrics
"""

__version__ = "1.0.0"
__author__ = "TRUTH Team"
__title__ = "TRUTH - Fake News Detection System"

# Package imports
from src.models.analyzer import ContentAnalyzer
from src.models.detector import FakeNewsDetector
from src.models.credibility import SourceCredibilityAnalyzer
from src.models.fact_checker import FactChecker
from src.utils.text_processor import TextPreprocessor, TextAnalyzer

__all__ = [
    'ContentAnalyzer',
    'FakeNewsDetector',
    'SourceCredibilityAnalyzer',
    'FactChecker',
    'TextPreprocessor',
    'TextAnalyzer',
]

if __name__ == '__main__':
    print(f"""
╔════════════════════════════════════════════════════════════╗
║  {__title__:50}     ║
║  {f"v{__version__}":50}     ║
║  {__author__:50}     ║
╚════════════════════════════════════════════════════════════╝

TRUTH System - Ready to detect fake news!

Quick Start:
  1. python demo.py              # See all features
  2. python test_system.py       # Run tests
  3. python -m flask --app api.app run   # Start server
  4. Open: http://localhost:5000

Documentation:
  - README.md: Full documentation
  - QUICKSTART.md: 5-minute setup
  - TRUTH_SUMMARY.md: Project overview

Learn More:
  - Import the analyzer: from src.models.analyzer import ContentAnalyzer
  - Check sample data: from data.sample_articles import get_sample_articles
  - Run the demo: python demo.py

Theme: TRUTH - Detect Misinformation, Uncover Truth
    """)
