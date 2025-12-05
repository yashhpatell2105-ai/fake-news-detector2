# TRUTH - Fake News Detection System - Copilot Instructions

## Project Overview

TRUTH is an AI-powered Fake News Detection System designed to combat misinformation by combining:
- Natural Language Processing for content analysis
- Source credibility verification
- Real-time fact-checking capabilities
- User-friendly web interface
- Comprehensive accuracy metrics

**Theme**: TRUTH - Uncovering facts in an information-rich world

## Project Structure

```
TRUTH/
├── api/                          # Flask REST API
│   ├── app.py                   # Main Flask application
│   └── __init__.py
├── src/                          # Source code
│   ├── config.py                # Configuration settings
│   ├── models/                  # AI/ML models
│   │   ├── analyzer.py          # Unified content analyzer
│   │   ├── detector.py          # Fake news detector
│   │   ├── credibility.py       # Source credibility
│   │   ├── fact_checker.py      # Fact-checking engine
│   │   └── __init__.py
│   ├── utils/                   # Utility modules
│   │   ├── text_processor.py    # NLP preprocessing
│   │   └── __init__.py
│   └── __init__.py
├── frontend/                    # Web UI
│   ├── index.html              # Main page
│   └── static/
│       ├── style.css           # Styling
│       └── script.js           # Frontend logic
├── data/                        # Data files
│   ├── sample_articles.py      # Test samples
│   └── __init__.py
├── .vscode/                     # VS Code config
│   ├── launch.json             # Debug config
│   └── settings.json           # Editor settings
├── demo.py                      # Demo script
├── requirements.txt             # Dependencies
├── .env                         # Environment config
├── .gitignore                   # Git ignore
└── README.md                    # Documentation
```

## Key Components

### 1. NLP Analysis (`src/utils/text_processor.py`)
- TextPreprocessor: Clean and normalize text
- TextAnalyzer: Sentiment analysis, language patterns
- Entity extraction and text statistics

### 2. Fake News Detection (`src/models/detector.py`)
- Machine Learning model (Random Forest)
- TF-IDF vectorization
- Training and prediction
- Model persistence

### 3. Credibility Verification (`src/models/credibility.py`)
- Domain verification
- SSL certificate checking
- Known source database
- Author credibility assessment

### 4. Fact-Checking (`src/models/fact_checker.py`)
- Claim extraction from text
- Fact-check database integration
- Multi-source verification
- Confidence scoring

### 5. Unified Analyzer (`src/models/analyzer.py`)
- Combines all verification methods
- Overall credibility scoring
- Comprehensive reporting
- Actionable recommendations

### 6. Flask API (`api/app.py`)
- RESTful endpoints for analysis
- Batch processing support
- Error handling
- CORS support

### 7. Web Interface (`frontend/`)
- Intuitive UI for news verification
- Tabbed analysis results
- Responsive design
- Real-time feedback

## Development Guidelines

### Code Standards
- Follow PEP 8 style guide
- Use meaningful variable/function names
- Add docstrings to all classes/functions
- Comment complex logic
- Type hints recommended

### Testing
- Use `demo.py` to test functionality
- Sample articles in `data/sample_articles.py`
- Test API endpoints manually or with Postman
- Check edge cases

### Configuration
- Edit `src/config.py` for system settings
- Use `.env` for environment variables
- Never commit sensitive keys
- Document config changes

## How to Run

### Setup
```bash
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

### Run Demo
```bash
python demo.py
```

### Run Web Server
```bash
python -m flask --app api.app run
# or with debug
set FLASK_ENV=development
python -m flask --app api.app run
```

### VS Code Debug
- Press F5 to run Flask server
- Or select "Python: Demo Script" from debug menu

## API Endpoints

### POST /api/analyze
Analyze single article
- Input: content, source_url (optional), author (optional)
- Output: Analysis report with credibility score

### POST /api/analyze/batch
Analyze multiple articles
- Input: Array of article objects
- Output: Array of analysis results

### POST /api/extract-claims
Extract claims from text
- Input: content
- Output: List of extracted claims

### POST /api/verify-claim
Verify specific claim
- Input: claim
- Output: Verdict, confidence, explanation

### POST /api/verify-source
Check source credibility
- Input: url
- Output: Credibility score and assessment

### GET /api/health
Health check endpoint

## Customization Points

### Expand Fact-Check Database
Edit `_initialize_fact_db()` in `fact_checker.py` to add more claims

### Add Trusted Sources
Modify `TRUSTED_SOURCES` in `credibility.py`

### Train Custom Model
Use `FakeNewsDetector.train()` with custom dataset

### Adjust Thresholds
Modify confidence thresholds in `config.py`

## Testing with Sample Data

The project includes 4 sample articles:
1. Real: Vaccine study
2. Fake: 5G conspiracy
3. Real: Climate report
4. Fake: Alien bases

Use `demo.py` to see how system analyzes them.

## Performance Considerations

- NLP operations are CPU-intensive
- Cache model predictions if needed
- Batch processing for multiple articles
- Rate limiting recommended for API

## Known Limitations

- Fact-check database is limited
- Model accuracy depends on training data
- Real sources are complex to verify
- Should supplement human judgment
- Requires regular model updates

## Next Steps for Enhancement

1. Integrate external fact-check APIs
2. Add more training data
3. Implement advanced NER
4. Support multiple languages
5. Add image/video verification
6. Mobile app development
7. Browser extension

## Dependencies

Core libraries in `requirements.txt`:
- Flask (web framework)
- scikit-learn (ML)
- NLTK (NLP)
- TextBlob (sentiment)
- NumPy/Pandas (data)
- requests (HTTP)

## Troubleshooting

**NLTK data missing**: Run `python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"`

**Port already in use**: Change PORT in `.env` or `src/config.py`

**Model not found**: First run will create default model, or use `demo.py`

**CORS errors**: Check CORS configuration in `api/app.py`

## Project Status

✅ Core functionality complete
✅ NLP analysis implemented
✅ Web interface working
✅ Demo script available
✅ Documentation complete

🔄 Ready for: Testing, deployment, enhancement

## Additional Notes

- This is an educational tool for fake news detection
- Not a replacement for professional fact-checking
- Always verify important claims with multiple sources
- Model should be retrained regularly with new data
- System transparency is important - show analysis process
