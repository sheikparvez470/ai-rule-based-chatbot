import re
from typing import List, Dict, Tuple
from collections import Counter

class NLPProcessor:
    """Natural Language Processing utilities for text analysis."""
    
    @staticmethod
    def tokenize(text: str) -> List[str]:
        """Split text into tokens (words)."""
        # Split by whitespace and punctuation
        tokens = re.findall(r'\b\w+\b', text.lower())
        return tokens
    
    @staticmethod
    def remove_stopwords(tokens: List[str]) -> List[str]:
        """Remove common English stopwords."""
        stopwords = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'from', 'is', 'are', 'was', 'were', 'be', 'been',
            'i', 'you', 'he', 'she', 'it', 'we', 'they', 'what', 'which', 'who',
            'when', 'where', 'why', 'how', 'do', 'does', 'did', 'can', 'could',
            'will', 'would', 'should', 'may', 'might', 'must', 'shall'
        }
        return [token for token in tokens if token not in stopwords]
    
    @staticmethod
    def get_word_frequency(text: str) -> Dict[str, int]:
        """Calculate word frequency in text."""
        tokens = NLPProcessor.tokenize(text)
        tokens = NLPProcessor.remove_stopwords(tokens)
        frequency = Counter(tokens)
        return dict(frequency.most_common())
    
    @staticmethod
    def get_keywords(text: str, top_n: int = 5) -> List[str]:
        """Extract top N keywords from text."""
        frequency = NLPProcessor.get_word_frequency(text)
        return [word for word, _ in sorted(frequency.items(), key=lambda x: x[1], reverse=True)[:top_n]]
    
    @staticmethod
    def detect_sentiment(text: str) -> Dict[str, float]:
        """Simple sentiment detection based on keywords."""
        text_lower = text.lower()
        
        positive_words = ['good', 'great', 'awesome', 'amazing', 'excellent', 'love',
                         'happy', 'glad', 'thanks', 'thank', 'wonderful', 'fantastic']
        negative_words = ['bad', 'terrible', 'awful', 'hate', 'angry', 'sad', 'upset',
                         'disappointed', 'poor', 'worst', 'horrible', 'disgusting']
        
        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)
        
        total = positive_count + negative_count
        if total == 0:
            return {'positive': 0.5, 'negative': 0.5, 'neutral': 0.0}
        
        positive_score = positive_count / total
        negative_score = negative_count / total
        
        return {
            'positive': positive_score,
            'negative': negative_score,
            'neutral': 1.0 - (positive_score + negative_score)
        }
    
    @staticmethod
    def detect_language(text: str) -> str:
        """Simple language detection (English, Spanish, French, etc.)."""
        # This is a very basic implementation
        # For production, use a library like 'textblob' or 'langdetect'
        spanish_indicators = ['hola', 'gracias', 'si', 'no', 'es', 'está']
        french_indicators = ['bonjour', 'merci', 'oui', 'non', 'est', 'le']
        
        text_lower = text.lower()
        spanish_count = sum(1 for word in spanish_indicators if word in text_lower)
        french_count = sum(1 for word in french_indicators if word in text_lower)
        
        if spanish_count > french_count and spanish_count > 0:
            return 'spanish'
        elif french_count > 0:
            return 'french'
        else:
            return 'english'
    
    @staticmethod
    def is_question(text: str) -> bool:
        """Detect if text is a question."""
        question_words = ['what', 'when', 'where', 'why', 'how', 'who', 'which', 'can', 'will', 'would']
        text_lower = text.lower().strip()
        
        # Check for question word at start
        for word in question_words:
            if text_lower.startswith(word):
                return True
        
        # Check for question mark
        if text.endswith('?'):
            return True
        
        return False
    
    @staticmethod
    def is_greeting(text: str) -> bool:
        """Detect if text is a greeting."""
        greetings = ['hello', 'hi', 'hey', 'greetings', 'good morning', 'good afternoon', 'good evening']
        text_lower = text.lower().strip()
        return any(greeting in text_lower for greeting in greetings)
    
    @staticmethod
    def normalize_text(text: str) -> str:
        """Normalize text for processing."""
        # Convert to lowercase
        text = text.lower()
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove special characters except punctuation
        text = re.sub(r'[^\w\s.!?,-]', '', text)
        return text.strip()
