#!/usr/bin/env python3
"""
Test script for the AI Rule-Based Chatbot.
"""

from utils.intent_matcher import IntentMatcher
from utils.entity_extractor import EntityExtractor
from utils.nlp_processor import NLPProcessor

def test_intent_matching():
    """Test intent matching functionality."""
    print("\n" + "="*60)
    print("Testing Intent Matching")
    print("="*60)
    
    matcher = IntentMatcher('data/intents.json')
    
    test_inputs = [
        "Hello!",
        "What's the weather?",
        "Goodbye!",
        "Can you help me?",
        "What time is it?"
    ]
    
    for user_input in test_inputs:
        response, confidence, intent = matcher.get_response(user_input)
        print(f"\nInput: {user_input}")
        print(f"Intent: {intent}")
        print(f"Confidence: {confidence:.2f}")
        print(f"Response: {response}")

def test_entity_extraction():
    """Test entity extraction functionality."""
    print("\n" + "="*60)
    print("Testing Entity Extraction")
    print("="*60)
    
    extractor = EntityExtractor('data/entities.json')
    
    test_inputs = [
        "My name is John and I live in New York",
        "I want to meet Alice in Paris tomorrow",
        "Can you give me 5 apples?",
        "The meeting is on Monday at 3 PM"
    ]
    
    for user_input in test_inputs:
        entities = extractor.extract_entities(user_input)
        print(f"\nInput: {user_input}")
        print(f"Entities: {entities}")

def test_nlp_processing():
    """Test NLP processing functionality."""
    print("\n" + "="*60)
    print("Testing NLP Processing")
    print("="*60)
    
    test_inputs = [
        "This is great! I love it!",
        "This is terrible and awful",
        "What is the capital of France?",
        "Hello! How are you?"
    ]
    
    for text in test_inputs:
        print(f"\nInput: {text}")
        
        # Tokenize
        tokens = NLPProcessor.tokenize(text)
        print(f"Tokens: {tokens}")
        
        # Keywords
        keywords = NLPProcessor.get_keywords(text, top_n=3)
        print(f"Keywords: {keywords}")
        
        # Sentiment
        sentiment = NLPProcessor.detect_sentiment(text)
        print(f"Sentiment: {sentiment}")
        
        # Question detection
        is_q = NLPProcessor.is_question(text)
        print(f"Is Question: {is_q}")

def test_full_conversation():
    """Test a full conversation flow."""
    print("\n" + "="*60)
    print("Testing Full Conversation Flow")
    print("="*60)
    
    matcher = IntentMatcher('data/intents.json')
    extractor = EntityExtractor('data/entities.json')
    
    conversation = [
        "Hello!",
        "What can you do?",
        "Tell me the time",
        "What's the weather in London?",
        "Goodbye!"
    ]
    
    print("\nConversation:")
    for user_input in conversation:
        response, confidence, intent = matcher.get_response(user_input)
        entities = extractor.extract_entities(user_input)
        
        print(f"\nUser: {user_input}")
        print(f"Bot: {response}")
        print(f"Intent: {intent} (Confidence: {confidence:.2f})")
        if entities:
            print(f"Entities: {entities}")

if __name__ == '__main__':
    print("\n🤖 AI RULE-BASED CHATBOT - TEST SUITE 🤖")
    
    try:
        test_intent_matching()
        test_entity_extraction()
        test_nlp_processing()
        test_full_conversation()
        
        print("\n" + "="*60)
        print("✓ All tests completed successfully!")
        print("="*60 + "\n")
    except Exception as e:
        print(f"\n✗ Test failed with error: {e}\n")
