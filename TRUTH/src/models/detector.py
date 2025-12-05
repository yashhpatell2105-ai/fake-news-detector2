"""Fake news detection model"""

import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
import pickle
import os

from src.utils.text_processor import TextPreprocessor


class FakeNewsDetector:
    """Detects fake news using NLP and ML techniques"""
    
    def __init__(self):
        self.model = None
        self.vectorizer = TfidfVectorizer(max_features=5000, stop_words='english')
        self.preprocessor = TextPreprocessor()
        self.model_path = "models/fake_news_detector.pkl"
    
    def train(self, texts, labels):
        """
        Train the fake news detection model
        
        Args:
            texts: List of text samples
            labels: List of labels (0 = fake, 1 = real)
        """
        # Preprocess texts
        cleaned_texts = [self.preprocessor.clean_text(text) for text in texts]
        
        # Vectorize texts
        X = self.vectorizer.fit_transform(cleaned_texts)
        y = np.array(labels)
        
        # Train Random Forest classifier
        self.model = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
        self.model.fit(X, y)
        
        return self
    
    def predict(self, text):
        """
        Predict if text is fake or real news
        
        Args:
            text: Input text to analyze
            
        Returns:
            Dictionary with prediction and confidence
        """
        if self.model is None:
            return {'error': 'Model not trained yet'}
        
        cleaned_text = self.preprocessor.clean_text(text)
        X = self.vectorizer.transform([cleaned_text])
        
        prediction = self.model.predict(X)[0]
        confidence = max(self.model.predict_proba(X)[0])
        
        return {
            'prediction': 'real' if prediction == 1 else 'fake',
            'confidence': float(confidence),
            'label': int(prediction)
        }
    
    def predict_batch(self, texts):
        """Make predictions for multiple texts"""
        results = []
        for text in texts:
            results.append(self.predict(text))
        return results
    
    def save_model(self, path=None):
        """Save trained model to disk"""
        path = path or self.model_path
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'wb') as f:
            pickle.dump({
                'model': self.model,
                'vectorizer': self.vectorizer
            }, f)
    
    def load_model(self, path=None):
        """Load trained model from disk"""
        path = path or self.model_path
        if os.path.exists(path):
            with open(path, 'rb') as f:
                data = pickle.load(f)
                self.model = data['model']
                self.vectorizer = data['vectorizer']
            return True
        return False
