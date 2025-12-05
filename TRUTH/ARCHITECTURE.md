# TRUTH - System Architecture & Components

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    User Interface Layer                      │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Web Interface (HTML/CSS/JS)                         │   │
│  │  - Responsive design                                │   │
│  │  - Real-time analysis results                        │   │
│  │  - Tabbed analysis views (Content/Source/Fact/Ling) │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                            ↓↑
┌─────────────────────────────────────────────────────────────┐
│                    API Layer (Flask)                         │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  REST Endpoints                                      │   │
│  │  /api/analyze          - Single article              │   │
│  │  /api/analyze/batch    - Multiple articles           │   │
│  │  /api/extract-claims   - Claim extraction            │   │
│  │  /api/verify-claim     - Claim verification          │   │
│  │  /api/verify-source    - Source verification         │   │
│  │  /api/health           - Health check                │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                            ↓↑
┌─────────────────────────────────────────────────────────────┐
│                 Analysis Engine Layer                        │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  ContentAnalyzer (Unified Interface)                │   │
│  │  ├── Combines all analysis methods                  │   │
│  │  ├── Aggregates scores                              │   │
│  │  └── Generates recommendations                      │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
    ↓↑                  ↓↑                  ↓↑                ↓↑
┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│   NLP Text   │  │ Fake News    │  │ Credibility  │  │  Fact-Check  │
│  Processing  │  │   Detector   │  │   Analyzer   │  │    Engine    │
├──────────────┤  ├──────────────┤  ├──────────────┤  ├──────────────┤
│ • Clean text │  │ • ML model   │  │ • Domain     │  │ • Extract    │
│ • Tokenize   │  │ • TF-IDF     │  │   check      │  │   claims     │
│ • Sentiment  │  │ • Classify   │  │ • SSL verify │  │ • Verify     │
│ • Patterns   │  │ • Confidence │  │ • Source DB  │  │   claims     │
│ • Entities   │  │ • Accuracy   │  │ • Author     │  │ • Confidence │
│ • Statistics │  │   metrics    │  │   check      │  │ • Evidence   │
└──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘
        ↓                ↓                  ↓                 ↓
┌─────────────────────────────────────────────────────────────┐
│                    Data Layer                                │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Configuration (config.py, .env)                    │   │
│  │  Sample Data (sample_articles.py)                   │   │
│  │  External Sources (APIs, Databases)                │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

## 📊 Analysis Pipeline

```
Input Article
    ↓
┌─────────────────────────────────────────┐
│   1. Text Preprocessing                 │
│   - Clean & normalize                   │
│   - Remove URLs, special chars          │
│   - Tokenize                            │
└─────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────┐
│   2. ML-Based Detection                 │
│   - Extract features (TF-IDF)           │
│   - Run Random Forest model             │
│   - Get prediction + confidence         │
└─────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────┐
│   3. Linguistic Analysis                │
│   - Sentiment analysis                  │
│   - Language patterns                   │
│   - Sensationalism scoring              │
│   - Readability check                   │
└─────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────┐
│   4. Source Verification                │
│   - Domain analysis                     │
│   - SSL certificate check               │
│   - Known sources lookup                │
│   - Author credibility                  │
└─────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────┐
│   5. Fact-Checking                      │
│   - Extract claims                      │
│   - Match against database              │
│   - Generate verdicts                   │
│   - Calculate confidence                │
└─────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────┐
│   6. Score Aggregation                  │
│   - Combine all scores                  │
│   - Weight results                      │
│   - Calculate overall score             │
│   - Generate recommendation             │
└─────────────────────────────────────────┘
    ↓
Output Report (JSON)
```

## 🔄 Component Interactions

```
┌─────────────────────────────────────────────────────────┐
│ Flask API (api/app.py)                                 │
│ ├─ Receives HTTP requests                             │
│ ├─ Validates input                                    │
│ └─ Routes to appropriate handler                      │
│         ↓                                              │
│    ContentAnalyzer                                     │
│    │                                                   │
│    ├─→ TextPreprocessor                               │
│    │   └─ Cleans input text                           │
│    │                                                   │
│    ├─→ TextAnalyzer                                   │
│    │   ├─ Sentiment analysis                          │
│    │   └─ Language patterns                           │
│    │                                                   │
│    ├─→ FakeNewsDetector                               │
│    │   ├─ Load model                                  │
│    │   ├─ Vectorize text (TF-IDF)                     │
│    │   └─ Predict + confidence                        │
│    │                                                   │
│    ├─→ SourceCredibilityAnalyzer                      │
│    │   ├─ Extract domain                              │
│    │   ├─ Verify SSL                                  │
│    │   └─ Check source database                       │
│    │                                                   │
│    └─→ FactChecker                                    │
│        ├─ Extract claims                              │
│        ├─ Verify claims                               │
│        └─ Get verdict + confidence                    │
│                                                        │
│    Aggregates all results                             │
│    └─ Combines scores                                 │
│    └─ Generates recommendation                        │
│         ↓                                              │
│    Returns JSON Response                              │
└─────────────────────────────────────────────────────────┘
```

## 📈 Data Flow Example

```
User Input:
{
    "content": "Article text here...",
    "source_url": "https://example.com",
    "author": "John Doe"
}
    ↓
API Processing:
    ├─ Validate input (min length check)
    ├─ Create ContentAnalyzer instance
    └─ Call analyze_news() method
        ↓
    Analysis Phase:
    ├─ Content Analysis:
    │  ├─ ML prediction: "real" (92% confidence)
    │  ├─ Sentiment: positive (0.2 polarity)
    │  ├─ Sensationalism: 20%
    │  └─ Readability: 85%
    │
    ├─ Source Analysis:
    │  ├─ Domain: example.com
    │  ├─ Credible: True
    │  └─ Score: 85%
    │
    ├─ Author Analysis:
    │  ├─ Unknown author
    │  └─ Score: 50%
    │
    └─ Fact-Checking:
       ├─ Claims found: 3
       ├─ Verified: 2 true, 1 false
       └─ Score: 67%
        ↓
    Aggregation:
    (0.92 + 0.85 + 0.5 + 0.67) / 4 = 0.74
    ├─ Overall Score: 74%
    ├─ Category: Good credibility
    └─ Recommendation: "Mixed signals, verify with other sources"
        ↓
JSON Response:
{
    "overall_score": 0.74,
    "content_analysis": {...},
    "source_analysis": {...},
    "author_analysis": {...},
    "fact_check": {...},
    "recommendation": "..."
}
```

## 🔐 Security & Error Handling

```
Request Handling:
┌─────────────────────────────────────────┐
│ 1. Receive Request                      │
│ 2. Validate JSON format                 │
│ 3. Check required fields                │
│ 4. Validate content length              │
│ 5. Sanitize inputs                      │
│ 6. Process safely                       │
│ 7. Handle exceptions                    │
│ 8. Return response/error                │
└─────────────────────────────────────────┘

Error Responses:
- 400: Bad request (invalid input)
- 404: Not found endpoint
- 500: Server error
- All include error messages
- Logging for debugging
```

## 💾 Model Persistence

```
Model Lifecycle:
1. Training Phase:
   detector.train(texts, labels)
   └─ Trains Random Forest on data
   └─ Stores TF-IDF vectorizer
   └─ Trains classification model
   
2. Saving:
   detector.save_model("path/to/model.pkl")
   └─ Pickles model and vectorizer
   └─ Saves to disk
   
3. Loading:
   detector.load_model("path/to/model.pkl")
   └─ Unpickles from disk
   └─ Loads into memory
   
4. Prediction:
   result = detector.predict(text)
   └─ Uses loaded vectorizer
   └─ Uses loaded model
   └─ Returns prediction + confidence
```

## 🎯 Scoring System

```
Component Scores (0-1):
├─ ML Detection: 0-1 (prediction confidence)
├─ Source Credibility: 0-1 (domain verification)
├─ Author Credibility: 0-1 (author check)
└─ Fact-Check: 0-1 (claim verification ratio)

Overall Score Calculation:
(ML_Score + Source_Score + Author_Score + FactCheck_Score) / 4

Score Ranges:
0.80-1.00: ✓ Credible (high confidence)
0.60-0.79: ⚠ Mixed (investigate further)
0.40-0.59: ⚠ Questionable (use caution)
0.00-0.39: ✗ Not credible (likely fake)

Recommendations Based on Score:
- ≥0.80: "✓ This appears to be credible news"
- 0.60-0.79: "⚠ Mixed signals, verify sources"
- 0.40-0.59: "⚠ Questionable elements, use caution"
- <0.40: "✗ Likely fake or low-credibility news"
```

## 🔍 Verification Methods

### NLP Analysis
- TextBlob sentiment (polarity, subjectivity)
- Language pattern detection (exclamations, caps, etc.)
- Sensationalism scoring (sensational words)
- Readability metrics
- Entity extraction (nouns, proper names)

### ML Detection
- Feature extraction via TF-IDF
- Random Forest classification
- Confidence scoring via probability
- Trained on fake/real examples

### Source Verification
- Domain name analysis
- SSL certificate checking
- Known source database
- Website structure analysis
- Author credibility lookup

### Fact-Checking
- Claim extraction via patterns
- Database matching
- Verdict assignment (True/False/Unknown)
- Confidence calculation
- Source tracking

## 📝 Logging & Monitoring

```
Application Logging:
- DEBUG: Detailed execution info
- INFO: General information
- WARNING: Warning messages
- ERROR: Error conditions

Log Levels (configurable):
- Edit LOG_LEVEL in src/config.py
- Default: INFO
- Options: DEBUG, INFO, WARNING, ERROR

Metrics Tracked:
- Request count
- Processing time
- Error rate
- Model accuracy
```

---

This architecture ensures robust, scalable, and maintainable fake news detection system.
