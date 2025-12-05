"""Real-time fact-checking capabilities"""

import requests
from datetime import datetime
from src.config import FACT_CHECK_THRESHOLD


class FactChecker:
    """Performs real-time fact-checking on claims"""
    
    def __init__(self):
        self.fact_check_db = self._initialize_fact_db()
    
    def _initialize_fact_db(self):
        """Initialize fact-check database with sample data"""
        return {
            'claim_vaccines_cause_autism': {
                'claim': 'Vaccines cause autism',
                'verdict': 'FALSE',
                'confidence': 0.99,
                'sources': ['WHO', 'CDC', 'Medical Research'],
                'explanation': 'Multiple large-scale studies have found no link between vaccines and autism'
            },
            'claim_5g_covid': {
                'claim': '5G networks caused COVID-19',
                'verdict': 'FALSE',
                'confidence': 0.99,
                'sources': ['WHO', 'IEEE', 'Scientific Community'],
                'explanation': 'COVID-19 is caused by SARS-CoV-2 virus, not electromagnetic radiation'
            },
            'claim_climate_change': {
                'claim': 'Climate change is real and caused by humans',
                'verdict': 'TRUE',
                'confidence': 0.97,
                'sources': ['IPCC', 'NASA', 'Scientific Consensus'],
                'explanation': '97% of climate scientists agree on human-caused climate change'
            },
            'claim_flat_earth': {
                'claim': 'Earth is flat',
                'verdict': 'FALSE',
                'confidence': 1.0,
                'sources': ['NASA', 'Science', 'Satellite Imagery'],
                'explanation': 'Multiple forms of evidence prove Earth is spherical'
            }
        }
    
    def extract_claims(self, text):
        """Extract potential claims from text"""
        # Simple claim extraction based on patterns
        claims = []
        sentences = text.split('.')
        
        for sentence in sentences:
            sentence = sentence.strip()
            if sentence and self._is_claim(sentence):
                claims.append(sentence)
        
        return claims[:5]  # Return top 5 claims
    
    def _is_claim(self, sentence):
        """Check if sentence is a factual claim"""
        claim_indicators = ['is', 'are', 'causes', 'caused', 'says', 'claims', 'states', 'proves']
        sentence_lower = sentence.lower()
        
        return any(indicator in sentence_lower for indicator in claim_indicators) and len(sentence) > 10
    
    def verify_claim(self, claim):
        """Verify a specific claim"""
        claim_lower = claim.lower()
        
        # Check against database
        for claim_key, fact_check in self.fact_check_db.items():
            if self._match_claim(claim_lower, fact_check['claim']):
                return {
                    'claim': claim,
                    'verdict': fact_check['verdict'],
                    'confidence': fact_check['confidence'],
                    'explanation': fact_check['explanation'],
                    'sources': fact_check['sources'],
                    'checked': True
                }
        
        # If not found, return uncertain
        return {
            'claim': claim,
            'verdict': 'UNKNOWN',
            'confidence': 0.0,
            'explanation': 'Claim not found in fact-check database',
            'sources': [],
            'checked': False
        }
    
    def _match_claim(self, claim1, claim2):
        """Check if two claims are similar"""
        # Simple substring matching
        claim2_lower = claim2.lower()
        keywords = claim2_lower.split()
        
        matching_keywords = sum(1 for keyword in keywords if keyword in claim1)
        match_ratio = matching_keywords / len(keywords) if keywords else 0
        
        return match_ratio >= 0.6
    
    def verify_claims_batch(self, claims):
        """Verify multiple claims"""
        results = []
        for claim in claims:
            result = self.verify_claim(claim)
            if result['confidence'] >= FACT_CHECK_THRESHOLD:
                results.append(result)
        
        return results
    
    def get_fact_check_score(self, text):
        """Get overall fact-check score for text"""
        claims = self.extract_claims(text)
        verified_claims = self.verify_claims_batch(claims)
        
        if not verified_claims:
            return {
                'score': 0.5,
                'reason': 'No verifiable claims found',
                'claims_checked': len(claims),
                'verified_claims': []
            }
        
        false_claims = sum(1 for c in verified_claims if c['verdict'] == 'FALSE')
        true_claims = sum(1 for c in verified_claims if c['verdict'] == 'TRUE')
        
        # Calculate score based on truth ratio
        truth_ratio = true_claims / len(verified_claims) if verified_claims else 0.5
        
        return {
            'score': truth_ratio,
            'reason': f'{true_claims} true vs {false_claims} false claims',
            'claims_checked': len(claims),
            'verified_claims': verified_claims
        }
