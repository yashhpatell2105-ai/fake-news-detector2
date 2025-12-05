"""Text analysis and preprocessing utilities"""

import re
import string
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from textblob import TextBlob

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')


class TextPreprocessor:
    """Handles text preprocessing and normalization"""
    
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))
    
    def clean_text(self, text):
        """Clean and normalize text"""
        # Convert to lowercase
        text = text.lower()
        # Remove URLs
        text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
        # Remove email addresses
        text = re.sub(r'\S+@\S+', '', text)
        # Remove special characters except spaces
        text = re.sub(f'[^{re.escape(string.ascii_letters + string.digits + " ")}]', '', text)
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        return text
    
    def tokenize_text(self, text):
        """Tokenize text into words"""
        return word_tokenize(text.lower())
    
    def remove_stopwords(self, tokens):
        """Remove common stopwords"""
        return [token for token in tokens if token not in self.stop_words and len(token) > 2]
    
    def get_sentences(self, text):
        """Extract sentences from text"""
        return sent_tokenize(text)
    
    def calculate_statistics(self, text):
        """Calculate text statistics"""
        words = self.tokenize_text(text)
        sentences = self.get_sentences(text)
        
        return {
            'word_count': len(words),
            'sentence_count': len(sentences),
            'avg_word_length': sum(len(w) for w in words) / len(words) if words else 0,
            'avg_sentence_length': len(words) / len(sentences) if sentences else 0,
            'unique_words': len(set(words))
        }


class TextAnalyzer:
    """Analyze text for linguistic patterns"""
    
    @staticmethod
    def get_sentiment(text):
        """Analyze sentiment using TextBlob"""
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity  # -1 to 1
        subjectivity = blob.sentiment.subjectivity  # 0 to 1
        
        return {
            'polarity': polarity,
            'subjectivity': subjectivity,
            'sentiment': 'positive' if polarity > 0.1 else 'negative' if polarity < -0.1 else 'neutral'
        }
    
    @staticmethod
    def analyze_language_patterns(text):
        """Analyze language patterns that may indicate fake news"""
        patterns = {
            'exclamation_count': text.count('!'),
            'question_count': text.count('?'),
            'caps_percentage': sum(1 for c in text if c.isupper()) / len(text) * 100 if text else 0,
            'quotation_count': text.count('"'),
            'has_sources': text.lower().count('according to') + text.lower().count('said') + text.lower().count('reported'),
            'sensational_words': sum(1 for word in ['shocking', 'amazing', 'incredible', 'unbelievable', 'devastating'] 
                                      if word in text.lower())
        }
        return patterns
    
    @staticmethod
    def extract_entities(text):
        """Extract key entities from text"""
        blob = TextBlob(text)
        nouns = [word for (word, tag) in blob.tags if tag.startswith('NN')]
        return list(set(nouns))[:10]  # Return top 10 unique nouns
