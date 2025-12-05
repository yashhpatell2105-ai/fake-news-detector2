"""Unified content analyzer combining all verification methods"""

from src.models.detector import FakeNewsDetector
from src.models.credibility import SourceCredibilityAnalyzer
from src.models.fact_checker import FactChecker
from src.utils.text_processor import TextAnalyzer, TextPreprocessor


class ContentAnalyzer:
    """Unified analyzer combining NLP, credibility, and fact-checking"""
    
    def __init__(self):
        self.detector = FakeNewsDetector()
        self.credibility_analyzer = SourceCredibilityAnalyzer()
        self.fact_checker = FactChecker()
        self.text_analyzer = TextAnalyzer()
        self.preprocessor = TextPreprocessor()
    
    def analyze_news(self, content, source_url=None, author=None):
        """
        Comprehensive analysis of news content
        
        Args:
            content: Article text
            source_url: Source URL (optional)
            author: Author name (optional)
            
        Returns:
            Detailed analysis report
        """
        report = {
            'content_analysis': self._analyze_content(content),
            'source_analysis': self._analyze_source(source_url),
            'author_analysis': self._analyze_author(author),
            'fact_check': self._fact_check_content(content),
            'overall_score': 0.0,
            'recommendation': ''
        }
        
        # Calculate overall score
        report['overall_score'] = self._calculate_overall_score(report)
        report['recommendation'] = self._generate_recommendation(report)
        
        return report
    
    def _analyze_content(self, content):
        """Analyze content characteristics"""
        try:
            # ML-based detection
            detector_result = self.detector.predict(content)
            
            # Linguistic analysis
            sentiment = self.text_analyzer.get_sentiment(content)
            language_patterns = self.text_analyzer.analyze_language_patterns(content)
            text_stats = self.preprocessor.calculate_statistics(content)
            
            return {
                'ml_prediction': detector_result['prediction'],
                'ml_confidence': detector_result['confidence'],
                'sentiment': sentiment,
                'language_patterns': language_patterns,
                'text_statistics': text_stats,
                'readability_score': self._calculate_readability(language_patterns),
                'sensationalism_score': self._calculate_sensationalism(language_patterns)
            }
        except Exception as e:
            return {'error': str(e)}
    
    def _analyze_source(self, source_url):
        """Analyze source credibility"""
        if not source_url:
            return {
                'url': None,
                'credible': None,
                'score': 0.5,
                'reason': 'No source URL provided'
            }
        
        return self.credibility_analyzer.verify_source(source_url)
    
    def _analyze_author(self, author):
        """Analyze author credibility"""
        if not author:
            return {
                'author': None,
                'credible': None,
                'score': 0.5,
                'reason': 'No author provided'
            }
        
        return self.credibility_analyzer.verify_author(author)
    
    def _fact_check_content(self, content):
        """Fact-check claims in content"""
        return self.fact_checker.get_fact_check_score(content)
    
    def _calculate_readability(self, patterns):
        """Calculate readability score based on patterns"""
        # Simple readability metric
        caps_percentage = patterns.get('caps_percentage', 0)
        exclamation_count = patterns.get('exclamation_count', 0)
        
        readability = 100 - (caps_percentage * 0.5 + exclamation_count * 2)
        return max(0, min(100, readability))
    
    def _calculate_sensationalism(self, patterns):
        """Calculate sensationalism score"""
        sensational_words = patterns.get('sensational_words', 0)
        exclamations = patterns.get('exclamation_count', 0)
        
        sensationalism = (sensational_words * 10 + exclamations * 5)
        return min(100, sensationalism)
    
    def _calculate_overall_score(self, report):
        """Calculate overall credibility score"""
        scores = []
        
        # Content score (inverted - lower fake probability = higher credibility)
        content = report['content_analysis']
        if 'ml_confidence' in content:
            if content['ml_prediction'] == 'real':
                scores.append(content['ml_confidence'])
            else:
                scores.append(1 - content['ml_confidence'])
        
        # Source score
        source = report['source_analysis']
        if 'score' in source:
            scores.append(source['score'])
        
        # Author score
        author = report['author_analysis']
        if author.get('credible') is True:
            scores.append(0.8)
        elif author.get('credible') is False:
            scores.append(0.2)
        else:
            scores.append(0.5)
        
        # Fact-check score
        fact_check = report['fact_check']
        if 'score' in fact_check:
            scores.append(fact_check['score'])
        
        return sum(scores) / len(scores) if scores else 0.5
    
    def _generate_recommendation(self, report):
        """Generate recommendation based on analysis"""
        score = report['overall_score']
        
        if score >= 0.8:
            return '✓ This appears to be credible news from a reliable source'
        elif score >= 0.6:
            return '⚠ This content has mixed credibility indicators. Verify with other sources'
        elif score >= 0.4:
            return '⚠ This content contains questionable elements. Use caution'
        else:
            return '✗ This appears to be low-credibility or potentially fake news'
