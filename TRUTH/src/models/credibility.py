"""Source credibility verification"""

import requests
from datetime import datetime
from src.config import API_TIMEOUT, MAX_SOURCES_TO_CHECK


class SourceCredibilityAnalyzer:
    """Analyzes source credibility and reliability"""
    
    # Known credible sources
    TRUSTED_SOURCES = {
        'bbc.com', 'reuters.com', 'apnews.com', 'theguardian.com',
        'nytimes.com', 'washingtonpost.com', 'bloomberg.com', 'ft.com',
        'cnn.com', 'bbc.co.uk', 'theja.org.za', 'news.google.com'
    }
    
    # Known unreliable sources
    UNTRUSTED_SOURCES = {
        'fake-news-site.com', 'misinformation.net', 'propaganda.org'
    }
    
    def __init__(self):
        self.credibility_scores = {}
    
    def extract_domain(self, url):
        """Extract domain from URL"""
        if not url:
            return None
        url = url.lower()
        # Remove protocol
        if '://' in url:
            url = url.split('://', 1)[1]
        # Remove path
        if '/' in url:
            url = url.split('/', 1)[0]
        # Remove www
        if url.startswith('www.'):
            url = url[4:]
        return url
    
    def verify_source(self, url):
        """Verify source credibility"""
        domain = self.extract_domain(url)
        
        if not domain:
            return {
                'credible': False,
                'score': 0.0,
                'reason': 'Invalid URL'
            }
        
        # Check against known sources
        if domain in self.TRUSTED_SOURCES:
            return {
                'credible': True,
                'score': 0.95,
                'reason': 'Known credible source'
            }
        
        if domain in self.UNTRUSTED_SOURCES:
            return {
                'credible': False,
                'score': 0.1,
                'reason': 'Known unreliable source'
            }
        
        # Try to fetch and analyze source
        return self._analyze_source_details(url, domain)
    
    def _analyze_source_details(self, url, domain):
        """Analyze source details for credibility"""
        try:
            response = requests.head(url, timeout=API_TIMEOUT, allow_redirects=True)
            
            factors = {
                'has_https': url.lower().startswith('https'),
                'status_ok': response.status_code == 200,
                'domain_age': self._estimate_domain_age(domain),
                'has_about': self._check_about_page(url)
            }
            
            score = self._calculate_credibility_score(factors)
            
            return {
                'credible': score >= 0.6,
                'score': score,
                'reason': self._get_credibility_reason(factors, score),
                'factors': factors
            }
        except Exception as e:
            return {
                'credible': False,
                'score': 0.3,
                'reason': f'Unable to verify source: {str(e)}'
            }
    
    def _estimate_domain_age(self, domain):
        """Estimate if domain is relatively new (suspicious if very new)"""
        # This is a placeholder - in production, use WHOIS lookup
        return 'unknown'
    
    def _check_about_page(self, url):
        """Check if source has an About page"""
        try:
            about_url = url.rstrip('/') + '/about'
            response = requests.get(about_url, timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def _calculate_credibility_score(self, factors):
        """Calculate overall credibility score"""
        score = 0.5  # Start with neutral
        
        if factors['has_https']:
            score += 0.15
        if factors['status_ok']:
            score += 0.2
        if factors['has_about']:
            score += 0.15
        
        return min(score, 1.0)
    
    def _get_credibility_reason(self, factors, score):
        """Generate reason for credibility score"""
        if score >= 0.8:
            return 'Source appears credible'
        elif score >= 0.6:
            return 'Source has reasonable credibility'
        elif score >= 0.4:
            return 'Source credibility is questionable'
        else:
            return 'Source credibility is low'
    
    def verify_author(self, author_name):
        """Verify if author is known and credible"""
        # Placeholder for author verification
        known_authors = {
            'reuters': 0.95,
            'bbc': 0.95,
            'associated press': 0.95
        }
        
        author_lower = author_name.lower() if author_name else ''
        for known_author, score in known_authors.items():
            if known_author in author_lower:
                return {
                    'credible': True,
                    'score': score,
                    'reason': f'Known credible author: {known_author}'
                }
        
        return {
            'credible': None,
            'score': 0.5,
            'reason': 'Author credibility unknown'
        }
