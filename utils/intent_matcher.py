import json
import re
from difflib import SequenceMatcher
from typing import Dict, List, Tuple
import random
from datetime import datetime

class IntentMatcher:
    """Matches user input to predefined intents using pattern matching and NLP."""
    
    def __init__(self, intents_file: str = "data/intents.json"):
        """
        Initialize the IntentMatcher with intents from a JSON file.
        
        Args:
            intents_file: Path to the intents JSON file
        """
        self.intents = self._load_intents(intents_file)
        self.context = {}
        
    def _load_intents(self, file_path: str) -> Dict:
        """Load intents from JSON file."""
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
                return data.get('intents', [])
        except FileNotFoundError:
            print(f"Warning: Intents file '{file_path}' not found.")
            return []
    
    def _preprocess_input(self, user_input: str) -> str:
        """Clean and normalize user input."""
        # Convert to lowercase
        text = user_input.lower().strip()
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove punctuation for matching (but keep original for context)
        return text
    
    def _extract_keywords(self, text: str) -> List[str]:
        """Extract keywords from text."""
        # Remove common words (stopwords)
        stopwords = {'is', 'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for'}
        words = text.split()
        return [w for w in words if w not in stopwords and len(w) > 2]
    
    def _calculate_similarity(self, user_text: str, pattern: str) -> float:
        """Calculate similarity between user input and pattern using SequenceMatcher."""
        return SequenceMatcher(None, user_text, pattern).ratio()
    
    def _match_intent(self, user_input: str) -> Tuple[str, float, Dict]:
        """Match user input to an intent and return intent ID, confidence, and intent data."""
        processed_input = self._preprocess_input(user_input)
        keywords = self._extract_keywords(processed_input)
        
        best_match = None
        best_confidence = 0
        best_intent = None
        
        for intent in self.intents:
            intent_id = intent.get('id')
            patterns = intent.get('patterns', [])
            threshold = intent.get('confidence_threshold', 0.6)
            
            # Check for keyword matches
            for pattern in patterns:
                if pattern in processed_input:
                    confidence = 1.0
                    if confidence > best_confidence:
                        best_confidence = confidence
                        best_match = intent_id
                        best_intent = intent
                    break
            
            # If no exact match, check similarity
            if best_confidence < 0.9:
                for pattern in patterns:
                    similarity = self._calculate_similarity(processed_input, pattern)
                    if similarity > best_confidence and similarity >= threshold:
                        best_confidence = similarity
                        best_match = intent_id
                        best_intent = intent
        
        return best_match, best_confidence, best_intent
    
    def get_response(self, user_input: str) -> Tuple[str, float, str]:
        """
        Get chatbot response based on user input.
        
        Returns:
            Tuple of (response_text, confidence_score, intent_id)
        """
        intent_id, confidence, intent_data = self._match_intent(user_input)
        
        if intent_id is None or confidence < 0.5:
            return self._get_fallback_response(), 0.0, "unknown"
        
        responses = intent_data.get('responses', [])
        response = random.choice(responses) if responses else "I'm not sure how to respond to that."
        
        # Replace placeholders
        response = self._replace_placeholders(response, intent_id)
        
        # Store in context
        self._update_context(user_input, response, intent_id, confidence)
        
        return response, confidence, intent_id
    
    def _replace_placeholders(self, response: str, intent_id: str) -> str:
        """Replace placeholders in response with actual values."""
        if "{time}" in response:
            current_time = datetime.now().strftime("%H:%M:%S")
            response = response.replace("{time}", current_time)
        
        if "{date}" in response:
            current_date = datetime.now().strftime("%A, %B %d, %Y")
            response = response.replace("{date}", current_date)
        
        if "{name}" in response:
            name = self.context.get('user_name', 'Friend')
            response = response.replace("{name}", name)
        
        return response
    
    def _update_context(self, user_input: str, response: str, intent_id: str, confidence: float) -> None:
        """Update conversation context."""
        if 'conversation_history' not in self.context:
            self.context['conversation_history'] = []
        
        self.context['conversation_history'].append({
            'user_input': user_input,
            'bot_response': response,
            'intent': intent_id,
            'confidence': confidence,
            'timestamp': datetime.now().isoformat()
        })
        
        # Keep only last 10 exchanges
        if len(self.context['conversation_history']) > 10:
            self.context['conversation_history'] = self.context['conversation_history'][-10:]
    
    def _get_fallback_response(self) -> str:
        """Return a fallback response when no intent matches."""
        fallback_responses = [
            "I'm not sure I understand. Could you rephrase that?",
            "I don't have information about that. Can you ask something else?",
            "That's interesting, but I'm not equipped to answer that. Try asking about something else.",
            "Hmm, I didn't catch that. Could you say it differently?",
            "I'm sorry, I don't understand. Can you provide more details?"
        ]
        return random.choice(fallback_responses)
    
    def get_context(self) -> Dict:
        """Return current conversation context."""
        return self.context
    
    def clear_context(self) -> None:
        """Clear conversation history."""
        self.context = {}
