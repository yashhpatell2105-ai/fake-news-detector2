#!/usr/bin/env python
"""
Test runner to verify TRUTH system components
Checks all modules can be imported and basic functionality works
"""

import sys
import traceback


def test_imports():
    """Test that all modules can be imported"""
    print("="*60)
    print("Testing Imports...")
    print("="*60)
    
    tests = [
        ("Config", "from src.config import DEBUG, HOST, PORT"),
        ("Text Processor", "from src.utils.text_processor import TextPreprocessor, TextAnalyzer"),
        ("Detector", "from src.models.detector import FakeNewsDetector"),
        ("Credibility", "from src.models.credibility import SourceCredibilityAnalyzer"),
        ("Fact Checker", "from src.models.fact_checker import FactChecker"),
        ("Analyzer", "from src.models.analyzer import ContentAnalyzer"),
        ("Flask App", "from api.app import app"),
        ("Sample Data", "from data.sample_articles import get_sample_articles"),
    ]
    
    passed = 0
    failed = 0
    
    for test_name, import_statement in tests:
        try:
            exec(import_statement)
            print(f"✓ {test_name}")
            passed += 1
        except Exception as e:
            print(f"✗ {test_name}: {e}")
            failed += 1
    
    print(f"\nImport Results: {passed} passed, {failed} failed")
    return failed == 0


def test_text_processor():
    """Test text processing functionality"""
    print("\n" + "="*60)
    print("Testing Text Processor...")
    print("="*60)
    
    try:
        from src.utils.text_processor import TextPreprocessor, TextAnalyzer
        
        # Test preprocessing
        preprocessor = TextPreprocessor()
        test_text = "Visit https://example.com! This is GREAT news!!!"
        cleaned = preprocessor.clean_text(test_text)
        assert len(cleaned) > 0, "Text cleaning failed"
        print("✓ Text cleaning works")
        
        # Test sentiment analysis
        analyzer = TextAnalyzer()
        sentiment = analyzer.get_sentiment("This is amazing!")
        assert 'polarity' in sentiment, "Sentiment analysis failed"
        print("✓ Sentiment analysis works")
        
        # Test language patterns
        patterns = analyzer.analyze_language_patterns("SHOCKING NEWS!!!")
        assert 'exclamation_count' in patterns, "Pattern analysis failed"
        print("✓ Language pattern analysis works")
        
        print("\n✓ Text Processor tests passed")
        return True
    except Exception as e:
        print(f"✗ Text Processor test failed: {e}")
        traceback.print_exc()
        return False


def test_models():
    """Test model functionality"""
    print("\n" + "="*60)
    print("Testing Models...")
    print("="*60)
    
    try:
        from src.models.detector import FakeNewsDetector
        from src.models.credibility import SourceCredibilityAnalyzer
        from src.models.fact_checker import FactChecker
        
        # Test detector
        detector = FakeNewsDetector()
        result = detector.predict("This is a test article about real news.")
        assert 'prediction' in result, "Detector prediction failed"
        assert 'confidence' in result, "Detector confidence failed"
        print("✓ Fake News Detector works")
        
        # Test credibility analyzer
        credibility = SourceCredibilityAnalyzer()
        result = credibility.verify_source("https://www.bbc.com")
        assert 'credible' in result, "Credibility analysis failed"
        print("✓ Source Credibility Analyzer works")
        
        # Test fact checker
        fact_checker = FactChecker()
        claims = fact_checker.extract_claims("Vaccines cause autism according to some.")
        assert isinstance(claims, list), "Claim extraction failed"
        print("✓ Fact Checker works")
        
        print("\n✓ Model tests passed")
        return True
    except Exception as e:
        print(f"✗ Model test failed: {e}")
        traceback.print_exc()
        return False


def test_analyzer():
    """Test unified analyzer"""
    print("\n" + "="*60)
    print("Testing Content Analyzer...")
    print("="*60)
    
    try:
        from src.models.analyzer import ContentAnalyzer
        
        analyzer = ContentAnalyzer()
        test_content = """
        According to the WHO, regular exercise is beneficial for health.
        Scientific studies show that 150 minutes per week is recommended.
        """
        
        analysis = analyzer.analyze_news(test_content, "https://www.who.int", "Dr. Jane")
        
        assert 'overall_score' in analysis, "Analysis missing overall score"
        assert 'content_analysis' in analysis, "Analysis missing content analysis"
        assert 'source_analysis' in analysis, "Analysis missing source analysis"
        assert 'recommendation' in analysis, "Analysis missing recommendation"
        
        print(f"✓ Analysis complete - Score: {analysis['overall_score']:.0%}")
        print(f"  Recommendation: {analysis['recommendation'][:50]}...")
        
        print("\n✓ Content Analyzer tests passed")
        return True
    except Exception as e:
        print(f"✗ Content Analyzer test failed: {e}")
        traceback.print_exc()
        return False


def test_api():
    """Test Flask API"""
    print("\n" + "="*60)
    print("Testing Flask API...")
    print("="*60)
    
    try:
        from api.app import app
        
        # Create test client
        client = app.test_client()
        
        # Test health endpoint
        response = client.get('/api/health')
        assert response.status_code == 200, "Health check failed"
        print("✓ Health check endpoint works")
        
        # Test analyze endpoint
        response = client.post('/api/analyze', 
            json={"content": "This is test content about real news."})
        assert response.status_code == 200, f"Analysis endpoint failed: {response.status_code}"
        print("✓ Analysis endpoint works")
        
        # Test extract claims endpoint
        response = client.post('/api/extract-claims',
            json={"content": "Vaccines cause autism."})
        assert response.status_code == 200, "Extract claims endpoint failed"
        print("✓ Extract claims endpoint works")
        
        # Test verify claim endpoint
        response = client.post('/api/verify-claim',
            json={"claim": "Climate change is real"})
        assert response.status_code == 200, "Verify claim endpoint failed"
        print("✓ Verify claim endpoint works")
        
        # Test verify source endpoint
        response = client.post('/api/verify-source',
            json={"url": "https://www.bbc.com"})
        assert response.status_code == 200, "Verify source endpoint failed"
        print("✓ Verify source endpoint works")
        
        print("\n✓ Flask API tests passed")
        return True
    except Exception as e:
        print(f"✗ API test failed: {e}")
        traceback.print_exc()
        return False


def test_sample_data():
    """Test sample data"""
    print("\n" + "="*60)
    print("Testing Sample Data...")
    print("="*60)
    
    try:
        from data.sample_articles import get_sample_articles, get_fake_articles, get_real_articles
        
        all_articles = get_sample_articles()
        fake_articles = get_fake_articles()
        real_articles = get_real_articles()
        
        assert len(all_articles) == 4, "Should have 4 sample articles"
        assert len(fake_articles) == 2, "Should have 2 fake articles"
        assert len(real_articles) == 2, "Should have 2 real articles"
        
        print(f"✓ Total articles: {len(all_articles)}")
        print(f"  - Real: {len(real_articles)}")
        print(f"  - Fake: {len(fake_articles)}")
        
        for article in all_articles:
            assert 'title' in article, "Article missing title"
            assert 'content' in article, "Article missing content"
            assert 'source' in article, "Article missing source"
            assert 'is_fake' in article, "Article missing is_fake flag"
        
        print("\n✓ Sample data tests passed")
        return True
    except Exception as e:
        print(f"✗ Sample data test failed: {e}")
        traceback.print_exc()
        return False


def main():
    """Run all tests"""
    print("\n")
    print("╔════════════════════════════════════════════════════════╗")
    print("║  TRUTH System - Component Tests                        ║")
    print("╚════════════════════════════════════════════════════════╝")
    
    results = []
    
    results.append(("Imports", test_imports()))
    results.append(("Text Processor", test_text_processor()))
    results.append(("Models", test_models()))
    results.append(("Content Analyzer", test_analyzer()))
    results.append(("Sample Data", test_sample_data()))
    results.append(("Flask API", test_api()))
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    for test_name, passed in results:
        status = "✓ PASSED" if passed else "✗ FAILED"
        print(f"{test_name:.<40} {status}")
    
    total_passed = sum(1 for _, passed in results if passed)
    total = len(results)
    
    print("="*60)
    print(f"Results: {total_passed}/{total} tests passed")
    
    if total_passed == total:
        print("\n🎉 All tests passed! System is ready to use.")
        print("\nNext steps:")
        print("1. Run: python demo.py")
        print("2. Run: python -m flask --app api.app run")
        print("3. Visit: http://localhost:5000")
        return 0
    else:
        print(f"\n⚠ {total - total_passed} test(s) failed. Check output above.")
        return 1


if __name__ == '__main__':
    sys.exit(main())
