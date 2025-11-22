"""
Market Sentiment Analyzer
"""

import logging
from typing import Dict, List, Any
from textblob import TextBlob

class SentimentAnalyzer:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def analyze_text_sentiment(self, text: str) -> Dict[str, Any]:
        """Analyze sentiment of text content"""
        try:
            blob = TextBlob(text)
            polarity = blob.sentiment.polarity
            subjectivity = blob.sentiment.subjectivity
            
            # Classify sentiment
            if polarity > 0.1:
                sentiment = "positive"
            elif polarity < -0.1:
                sentiment = "negative"
            else:
                sentiment = "neutral"
            
            return {
                'sentiment': sentiment,
                'polarity': polarity,
                'subjectivity': subjectivity,
                'confidence': abs(polarity)
            }
        except Exception as e:
            self.logger.error(f"Error analyzing text sentiment: {e}")
            return {
                'sentiment': 'neutral',
                'polarity': 0.0,
                'subjectivity': 0.0,
                'confidence': 0.0
            }
    
    def aggregate_sentiment(self, sentiments: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Aggregate multiple sentiment scores"""
        if not sentiments:
            return {
                'overall_sentiment': 'neutral',
                'average_polarity': 0.0,
                'average_confidence': 0.0
            }
        
        total_polarity = sum(s['polarity'] for s in sentiments)
        total_confidence = sum(s['confidence'] for s in sentiments)
        
        avg_polarity = total_polarity / len(sentiments)
        avg_confidence = total_confidence / len(sentiments)
        
        if avg_polarity > 0.1:
            overall_sentiment = "positive"
        elif avg_polarity < -0.1:
            overall_sentiment = "negative"
        else:
            overall_sentiment = "neutral"
        
        return {
            'overall_sentiment': overall_sentiment,
            'average_polarity': avg_polarity,
            'average_confidence': avg_confidence
        }
