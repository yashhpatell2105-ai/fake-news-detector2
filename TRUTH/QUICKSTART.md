# TRUTH - Quick Start Guide

## 🚀 Getting Started in 5 Minutes

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Download NLP Data (First Time Only)
```bash
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"
```

### Step 3: Run the Demo
```bash
python demo.py
```

This will show you all the system capabilities with sample data.

### Step 4: Start the Web Server
```bash
python -m flask --app api.app run
```

### Step 5: Open in Browser
```
http://localhost:5000
```

## 📊 What You Can Do

### In the Web Interface
1. **Paste news content** - Add article text to analyze
2. **Optional: Add source URL** - System will verify domain credibility
3. **Optional: Add author name** - System will check author credibility
4. **Click "Analyze Content"** - Get comprehensive analysis report

### In the API
Make POST requests to:
- `/api/analyze` - Single article analysis
- `/api/extract-claims` - Extract claims from text
- `/api/verify-claim` - Check specific claims
- `/api/verify-source` - Verify source credibility

## 🧪 Test Data

Use the sample articles to test:

```python
python -c "from data.sample_articles import get_sample_articles; 
print('\n'.join([f\"{i}. {a['title']}\" for i, a in enumerate(get_sample_articles(), 1)]))"
```

## 📈 Results Explained

**Credibility Score**
- 80-100%: Credible news ✓
- 60-79%: Mixed signals ⚠
- 40-59%: Questionable ⚠
- 0-39%: Likely fake ✗

**Tabs in Results**
- **Content**: ML analysis, sentiment, sensationalism
- **Source**: Domain credibility, SSL verification
- **Fact Check**: Claim verdicts, sources
- **Linguistic**: Language patterns, text statistics

## 🔧 Customization

### Change API Port
Edit `.env`:
```
PORT=8000
```

### Add More Fact-Checks
Edit `src/models/fact_checker.py` - `_initialize_fact_db()` method

### Adjust Confidence Thresholds
Edit `src/config.py`:
```python
MIN_CONFIDENCE_SCORE = 0.6  # Increase for stricter detection
```

## 🐛 Troubleshooting

**Port 5000 already in use?**
```bash
python -m flask --app api.app run --port 5001
```

**NLTK data errors?**
```bash
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"
```

**Module not found?**
```bash
# Make sure you're in the TRUTH directory
cd path/to/TRUTH
python demo.py
```

## 📚 Project Files

| File | Purpose |
|------|---------|
| `api/app.py` | Flask web server and API |
| `src/models/detector.py` | Fake news ML model |
| `src/models/credibility.py` | Source verification |
| `src/models/fact_checker.py` | Fact-checking engine |
| `src/utils/text_processor.py` | NLP analysis |
| `frontend/index.html` | Web interface |
| `frontend/static/` | CSS and JavaScript |
| `demo.py` | Demo script |
| `data/sample_articles.py` | Test data |

## ✨ Features at a Glance

✅ Machine Learning fake news detection
✅ Source credibility verification
✅ Fact-checking with confidence scoring
✅ Sentiment and linguistic analysis
✅ Language pattern detection
✅ Entity extraction
✅ User-friendly web interface
✅ RESTful API endpoints
✅ Batch processing
✅ Comprehensive metrics

## 🎯 Next Steps

1. **Run demo.py** to see all features
2. **Analyze sample articles** in the web interface
3. **Test the API** with curl or Postman
4. **Customize settings** in `src/config.py`
5. **Add your own data** to `data/sample_articles.py`

## 📖 Full Documentation

See `README.md` for comprehensive documentation.

---

**Need help?** Check the README.md or examine the demo.py output.
