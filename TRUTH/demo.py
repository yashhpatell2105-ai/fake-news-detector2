"""Demo script to test TRUTH system functionality"""

import sys
sys.path.insert(0, '.')

from src.models.analyzer import ContentAnalyzer
from src.utils.text_processor import TextPreprocessor
from data.sample_articles import get_sample_articles
import json


def print_section(title):
    """Print a formatted section header"""
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60 + "\n")


def demo_text_preprocessing():
    """Demonstrate text preprocessing"""
    print_section("Text Preprocessing Demo")
    
    preprocessor = TextPreprocessor()
    sample_text = "Visit https://example.com or email test@example.com! This is GREAT news!!!"
    
    print("Original text:")
    print(f"  {sample_text}\n")
    
    cleaned = preprocessor.clean_text(sample_text)
    print("Cleaned text:")
    print(f"  {cleaned}\n")
    
    stats = preprocessor.calculate_statistics(cleaned)
    print("Text statistics:")
    for key, value in stats.items():
        print(f"  {key}: {value}")


def demo_content_analysis():
    """Demonstrate content analysis"""
    print_section("Content Analysis Demo")
    
    from src.utils.text_processor import TextAnalyzer
    
    test_text = """
    BREAKING NEWS!!! Scientists have FINALLY discovered that eating apples causes allergies!!!
    This is SHOCKING and the media doesn't want you to know! Wake up sheeple!
    """
    
    analyzer = TextAnalyzer()
    
    print("Analyzing text:")
    print(f"  {test_text.strip()}\n")
    
    sentiment = analyzer.get_sentiment(test_text)
    print("Sentiment Analysis:")
    print(f"  {json.dumps(sentiment, indent=2)}\n")
    
    patterns = analyzer.analyze_language_patterns(test_text)
    print("Language Patterns:")
    print(f"  {json.dumps(patterns, indent=2)}\n")
    
    entities = analyzer.extract_entities(test_text)
    print(f"Extracted Entities: {entities}")


def demo_fake_news_detection():
    """Demonstrate fake news detection"""
    print_section("Fake News Detection Demo")
    
    detector = analyzer.detector
    
    # Real news
    real_text = """
    According to the CDC, regular exercise reduces the risk of heart disease. 
    Studies show that 150 minutes of moderate activity per week provides significant health benefits.
    """
    
    print("Sample Real News:")
    print(f"  {real_text}\n")
    result = detector.predict(real_text)
    print(f"Prediction: {result['prediction']}")
    print(f"Confidence: {result['confidence']:.2%}\n")
    
    # Fake news
    fake_text = """
    INCREDIBLE!!! Scientists PROVE that water has memory and can cure EVERYTHING!!!
    Governments are HIDING this TRUTH from you! THIS WILL SHOCK YOU!!!
    """
    
    print("Sample Fake News:")
    print(f"  {fake_text}\n")
    result = detector.predict(fake_text)
    print(f"Prediction: {result['prediction']}")
    print(f"Confidence: {result['confidence']:.2%}")


def demo_source_credibility():
    """Demonstrate source credibility verification"""
    print_section("Source Credibility Verification Demo")
    
    credibility = analyzer.credibility_analyzer
    
    test_urls = [
        "https://www.bbc.com/news/article",
        "https://www.example-fake-news.com/article",
        "https://github.com"
    ]
    
    for url in test_urls:
        print(f"Checking: {url}")
        result = credibility.verify_source(url)
        print(f"  Credible: {result.get('credible')}")
        print(f"  Score: {result.get('score', 0):.2%}")
        print(f"  Reason: {result.get('reason')}\n")


def demo_fact_checking():
    """Demonstrate fact checking"""
    print_section("Fact Checking Demo")
    
    fact_checker = analyzer.fact_checker
    
    test_text = """
    Vaccines cause autism. 5G networks caused COVID-19. Climate change isn't real.
    Earth is flat according to recent studies.
    """
    
    print("Analyzing claims in text...")
    print(f"  {test_text}\n")
    
    claims = fact_checker.extract_claims(test_text)
    print(f"Extracted {len(claims)} claims:\n")
    
    for i, claim in enumerate(claims, 1):
        print(f"{i}. \"{claim}\"")
        result = fact_checker.verify_claim(claim)
        print(f"   Verdict: {result['verdict']}")
        print(f"   Confidence: {result['confidence']:.0%}\n")


def demo_comprehensive_analysis():
    """Demonstrate comprehensive content analysis"""
    print_section("Comprehensive Content Analysis Demo")
    
    sample = get_sample_articles()[0]  # Real article
    
    print(f"Article: {sample['title']}")
    print(f"Source: {sample['source']}\n")
    
    analysis = analyzer.analyze_news(
        content=sample['content'],
        source_url=sample['source'],
        author="Sample Author"
    )
    
    print(f"Overall Credibility Score: {analysis['overall_score']:.0%}")
    print(f"Recommendation: {analysis['recommendation']}\n")
    
    print("Content Analysis:")
    content = analysis['content_analysis']
    print(f"  ML Prediction: {content.get('ml_prediction', 'N/A')}")
    print(f"  Confidence: {content.get('ml_confidence', 0):.0%}")
    print(f"  Sentiment: {content.get('sentiment', {}).get('sentiment', 'N/A')}")
    print(f"  Sensationalism: {content.get('sensationalism_score', 0):.0f}%\n")
    
    print("Source Analysis:")
    source = analysis['source_analysis']
    print(f"  Credible: {source.get('credible')}")
    print(f"  Score: {source.get('score', 0):.0%}\n")
    
    print("Fact-Check Summary:")
    fact_check = analysis['fact_check']
    print(f"  Claims Checked: {fact_check.get('claims_checked', 0)}")
    print(f"  Score: {fact_check.get('score', 0):.0%}")


def demo_all_sample_articles():
    """Analyze all sample articles"""
    print_section("Demo: Analyzing Sample Articles")
    
    articles = get_sample_articles()
    
    for i, article in enumerate(articles, 1):
        print(f"\n[{i}/{len(articles)}] {article['title']}")
        print(f"Expected: {'FAKE' if article['is_fake'] else 'REAL'}")
        
        analysis = analyzer.analyze_news(
            content=article['content'],
            source_url=article['source']
        )
        
        score = analysis['overall_score']
        prediction = "FAKE" if score < 0.5 else "REAL"
        
        print(f"Predicted: {prediction}")
        print(f"Confidence: {score:.0%}")
        print("-" * 40)


# Create analyzer instance globally
analyzer = ContentAnalyzer()


def main():
    """Run all demos"""
    print("\n")
    print("╔════════════════════════════════════════════════════════╗")
    print("║  TRUTH - Fake News Detection System Demo               ║")
    print("║  AI-Powered Misinformation Detection                  ║")
    print("╚════════════════════════════════════════════════════════╝")
    
    try:
        demo_text_preprocessing()
        demo_content_analysis()
        demo_fake_news_detection()
        demo_source_credibility()
        demo_fact_checking()
        demo_comprehensive_analysis()
        demo_all_sample_articles()
        
        print("\n" + "="*60)
        print("  Demo Complete!")
        print("="*60)
        print("\nTo start the web interface, run:")
        print("  python -m flask run")
        print("\nThen visit: http://localhost:5000")
        
    except Exception as e:
        print(f"\n❌ Demo error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
