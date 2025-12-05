# TRUTH - Fake News Detection System

**TRUTH** is an AI-powered system designed to detect and combat misinformation and fake news in digital media. It combines Natural Language Processing, source credibility verification, and real-time fact-checking to provide users with accurate assessments of news content credibility.

## Theme: TRUTH

The system embodies the core principle of uncovering truth in an information-saturated world where misinformation spreads rapidly.

## Features

### 1. **Natural Language Processing (NLP) Analysis**
- Sentiment analysis using TextBlob
- Language pattern detection
- Sensationalism scoring
- Entity extraction
- Text statistics and readability metrics

### 2. **Source Credibility Verification**
- Domain verification and analysis
- SSL certificate checking
- Known source database
- Author credibility assessment
- Website structure analysis

### 3. **Real-Time Fact-Checking**
- Claim extraction from articles
- Fact-check database integration
- Confidence scoring
- Source citations
- Multi-source verification

### 4. **Machine Learning Detection**
- Random Forest classifier for fake news detection
- TF-IDF vectorization
- Confidence scoring
- Model persistence and retraining

### 5. **User-Friendly Web Interface**
- Intuitive news verification form
- Real-time analysis results
- Tabbed analysis views
- Visual credibility scoring
- Responsive design

### 6. **Comprehensive Metrics**
- Overall credibility score (0-100%)
- Confidence percentages
- Detailed analysis breakdowns
- Actionable recommendations

## Project Structure

```
TRUTH/
├── api/
│   ├── __init__.py
│   └── app.py                 # Flask API server
├── src/
│   ├── __init__.py
│   ├── config.py              # Configuration settings
│   ├── models/
│   │   ├── __init__.py
│   │   ├── analyzer.py        # Unified content analyzer
│   │   ├── detector.py        # Fake news detector
│   │   ├── credibility.py     # Source credibility analyzer
│   │   └── fact_checker.py    # Fact-checking module
│   └── utils/
│       ├── __init__.py
│       └── text_processor.py  # Text processing utilities
├── frontend/
│   ├── index.html             # Main web interface
│   └── static/
│       ├── style.css          # Styling
│       └── script.js          # Frontend logic
├── data/
│   └── sample_articles.py     # Sample test data
├── demo.py                    # Demo script
├── requirements.txt           # Python dependencies
└── README.md                  # Documentation
```

## Installation

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Setup

1. **Clone or extract the project**
   ```bash
   cd TRUTH
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Download NLTK data** (first time only)
   ```bash
   python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"
   ```

## Usage

### Web Interface

1. **Start the Flask server**
   ```bash
   python -m flask --app api.app run
   ```

2. **Open in browser**
   ```
   http://localhost:5000
   ```

3. **Analyze news**
   - Paste article content
   - (Optional) Add source URL
   - (Optional) Add author name
   - Click "Analyze Content"

### Demo Script

Run the demo to see all features in action:

```bash
python demo.py
```

The demo includes:
- Text preprocessing examples
- Content analysis demonstration
- Fake news detection samples
- Source credibility verification
- Fact-checking examples
- Comprehensive article analysis

### API Endpoints

#### Analyze Single Article
```
POST /api/analyze
Content-Type: application/json

{
    "content": "Article text...",
    "source_url": "https://example.com/article",
    "author": "John Doe"
}

Response: {
    "success": true,
    "analysis": {
        "overall_score": 0.85,
        "content_analysis": {...},
        "source_analysis": {...},
        "fact_check": {...},
        "recommendation": "..."
    }
}
```

#### Extract Claims
```
POST /api/extract-claims
Content-Type: application/json

{
    "content": "Article text..."
}

Response: {
    "success": true,
    "claims": ["Claim 1", "Claim 2", ...],
    "count": 5
}
```

#### Verify Claim
```
POST /api/verify-claim
Content-Type: application/json

{
    "claim": "Claim to verify"
}

Response: {
    "success": true,
    "result": {
        "verdict": "FALSE",
        "confidence": 0.95,
        "explanation": "...",
        "sources": ["WHO", "CDC"]
    }
}
```

#### Verify Source
```
POST /api/verify-source
Content-Type: application/json

{
    "url": "https://example.com"
}

Response: {
    "success": true,
    "result": {
        "credible": true,
        "score": 0.85,
        "reason": "..."
    }
}
```

## Analysis Metrics

### Overall Credibility Score
- **80-100%**: Credible news from reliable sources
- **60-79%**: Mixed credibility indicators, verify with other sources
- **40-59%**: Questionable elements, use caution
- **0-39%**: Low-credibility or potentially fake news

### Content Analysis
- **ML Prediction**: Machine learning model prediction (Real/Fake)
- **Confidence**: Confidence score of the prediction
- **Sentiment**: Emotional tone (Positive/Negative/Neutral)
- **Sensationalism Score**: Level of sensational language
- **Readability**: Text readability percentage

### Source Analysis
- **Credibility**: Source trustworthiness
- **Score**: Numeric credibility rating
- **Factors**: Domain age, SSL status, About page

### Linguistic Analysis
- **Exclamation Marks**: Count of ! marks
- **CAPS Usage**: Percentage of uppercase text
- **Sensational Words**: Count of sensational vocabulary
- **Source References**: Number of citations

### Fact-Checking
- **Verdicts**: TRUE, FALSE, or UNKNOWN
- **Claims Checked**: Number of verifiable claims
- **Confidence**: Certainty of each verdict

## Sample Test Articles

The system includes 4 sample articles (2 real, 2 fake) for testing:

1. **Real**: Vaccine effectiveness study
2. **Fake**: 5G mutations conspiracy
3. **Real**: Climate change report
4. **Fake**: Alien underground bases

Use `python demo.py` to analyze these samples.

## Requirements

### Core Libraries
- **Flask**: Web framework
- **NumPy & Pandas**: Data processing
- **Scikit-learn**: Machine learning
- **NLTK**: Natural language processing
- **TextBlob**: Sentiment analysis
- **Requests**: HTTP requests

See `requirements.txt` for complete list.

## Configuration

Edit `src/config.py` to customize:
- Debug mode
- Server host/port
- NLP model settings
- Fact-check thresholds
- API timeouts
- Logging levels

## Model Training

The system uses a pre-trained Random Forest classifier. To train on custom data:

```python
from src.models.detector import FakeNewsDetector

detector = FakeNewsDetector()
texts = ["Article 1", "Article 2", ...]
labels = [1, 0, ...]  # 1=real, 0=fake

detector.train(texts, labels)
detector.save_model("models/custom_model.pkl")
```

## Extensibility

### Add Custom Fact-Checks
Edit `src/models/fact_checker.py` and add to `_initialize_fact_db()`:

```python
'claim_key': {
    'claim': 'Claim text',
    'verdict': 'TRUE/FALSE',
    'confidence': 0.95,
    'sources': ['Source 1', 'Source 2'],
    'explanation': 'Explanation'
}
```

### Add Credible Sources
Edit `src/models/credibility.py` and add domains to `TRUSTED_SOURCES` or `UNTRUSTED_SOURCES`.

### Integrate External APIs
Modify `FactChecker` and `SourceCredibilityAnalyzer` to call external fact-check APIs.

## Limitations & Disclaimers

- Model accuracy depends on training data quality
- Fact-check database is limited and requires constant updates
- Real-world sources are complex and may not be fully verifiable
- System provides analysis aids, not definitive truth
- Should be used alongside human judgment
- No system can catch all misinformation perfectly

## Future Enhancements

- [ ] Integration with fact-check APIs (Snopes, FactCheck.org)
- [ ] Multi-language support
- [ ] Real-time news source monitoring
- [ ] Machine learning model retraining pipeline
- [ ] Advanced claim extraction with NER
- [ ] Image and video verification
- [ ] Blockchain-based source verification
- [ ] User feedback and model improvement
- [ ] Mobile application
- [ ] Browser extension

## Contributing

Contributions welcome! Areas for improvement:
- Better fake news detection models
- Expanded fact-check database
- Additional verification methods
- Performance optimization
- UI/UX improvements

## License

This project is provided as an educational tool for fake news detection.

## Support & Contact

For issues, questions, or suggestions, please refer to the project documentation or contact the development team.

---

**Remember**: TRUTH is about uncovering facts in an information-rich world. Use this system responsibly and always verify important claims through multiple reliable sources.

**Last Updated**: December 2024
