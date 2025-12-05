"""Flask API for TRUTH - Fake News Detection System"""

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import logging
import os
from datetime import datetime

from src.config import DEBUG, HOST, PORT, SECRET_KEY, LOG_LEVEL
from src.models.analyzer import ContentAnalyzer
import nltk
import ssl

# Configure logging
logging.basicConfig(level=getattr(logging, LOG_LEVEL))
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__, template_folder='../frontend', static_folder='../frontend/static')
app.config['SECRET_KEY'] = SECRET_KEY
CORS(app)

# Ensure required NLTK data is available (download if missing)
try:
    try:
        _create_unverified_https_context = ssl._create_unverified_context
    except AttributeError:
        pass
    else:
        ssl._create_default_https_context = _create_unverified_https_context

    required_nltk = ['punkt', 'stopwords', 'averaged_perceptron_tagger', 'wordnet']
    for res in required_nltk:
        try:
            nltk.data.find(res if '/' in res else f"tokenizers/{res}" if res == 'punkt' else f"corpora/{res}")
        except LookupError:
            logger.info(f"NLTK resource '{res}' not found. Downloading...")
            nltk.download(res)
except Exception:
    logger.exception("Failed to verify/download NLTK data")

# Initialize analyzer
analyzer = ContentAnalyzer()

# Try to load pre-trained model
try:
    if analyzer.detector.load_model():
        logger.info("Pre-trained model loaded successfully")
    else:
        logger.warning("No pre-trained model found - using default analysis")
except Exception as e:
    logger.warning(f"Could not load model: {e}")


@app.route('/')
def index():
    """Serve the main page"""
    return render_template('index.html')


@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    }), 200


@app.route('/api/analyze', methods=['POST'])
def analyze_news():
    """
    Analyze news content for credibility
    
    Expected JSON:
    {
        "content": "Article text...",
        "source_url": "https://example.com/article",
        "author": "John Doe"
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
        
        content = data.get('content', '')
        source_url = data.get('source_url')
        author = data.get('author')
        
        if not content or len(content) < 10:
            return jsonify({'error': 'Content too short. Minimum 10 characters required.'}), 400
        
        # Perform analysis
        analysis_result = analyzer.analyze_news(content, source_url, author)
        
        return jsonify({
            'success': True,
            'analysis': analysis_result,
            'timestamp': datetime.now().isoformat()
        }), 200
        
    except Exception as e:
        logger.error(f"Analysis error: {str(e)}")
        return jsonify({
            'error': 'Analysis failed',
            'details': str(e)
        }), 500


@app.route('/api/analyze/batch', methods=['POST'])
def analyze_batch():
    """
    Analyze multiple news items
    
    Expected JSON:
    {
        "items": [
            {
                "content": "Article text...",
                "source_url": "https://example.com/article",
                "author": "John Doe"
            },
            ...
        ]
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'items' not in data:
            return jsonify({'error': 'Missing items array'}), 400
        
        items = data['items']
        if not isinstance(items, list) or len(items) == 0:
            return jsonify({'error': 'Items must be a non-empty array'}), 400
        
        if len(items) > 50:
            return jsonify({'error': 'Maximum 50 items per request'}), 400
        
        results = []
        for item in items:
            try:
                analysis = analyzer.analyze_news(
                    item.get('content', ''),
                    item.get('source_url'),
                    item.get('author')
                )
                results.append({
                    'analysis': analysis,
                    'success': True
                })
            except Exception as e:
                results.append({
                    'error': str(e),
                    'success': False
                })
        
        return jsonify({
            'success': True,
            'results': results,
            'timestamp': datetime.now().isoformat()
        }), 200
        
    except Exception as e:
        logger.error(f"Batch analysis error: {str(e)}")
        return jsonify({
            'error': 'Batch analysis failed',
            'details': str(e)
        }), 500


@app.route('/api/extract-claims', methods=['POST'])
def extract_claims():
    """Extract claims from text"""
    try:
        data = request.get_json()
        content = data.get('content', '')
        
        if not content:
            return jsonify({'error': 'No content provided'}), 400
        
        claims = analyzer.fact_checker.extract_claims(content)
        
        return jsonify({
            'success': True,
            'claims': claims,
            'count': len(claims)
        }), 200
        
    except Exception as e:
        logger.error(f"Claim extraction error: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/verify-claim', methods=['POST'])
def verify_claim():
    """Verify a specific claim"""
    try:
        data = request.get_json()
        claim = data.get('claim', '')
        
        if not claim:
            return jsonify({'error': 'No claim provided'}), 400
        
        result = analyzer.fact_checker.verify_claim(claim)
        
        return jsonify({
            'success': True,
            'result': result
        }), 200
        
    except Exception as e:
        logger.error(f"Claim verification error: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/verify-source', methods=['POST'])
def verify_source():
    """Verify source credibility"""
    try:
        data = request.get_json()
        url = data.get('url', '')
        
        if not url:
            return jsonify({'error': 'No URL provided'}), 400
        
        result = analyzer.credibility_analyzer.verify_source(url)
        
        return jsonify({
            'success': True,
            'result': result
        }), 200
        
    except Exception as e:
        logger.error(f"Source verification error: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Endpoint not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    logger.error(f"Internal error: {str(error)}")
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    app.run(host=HOST, port=PORT, debug=DEBUG)
