#!/usr/bin/env python3
"""
Command-line interface for the AI Rule-Based Chatbot.
Allows interactive conversation with the chatbot.
"""

import sys
from utils.intent_matcher import IntentMatcher
from utils.entity_extractor import EntityExtractor
from utils.nlp_processor import NLPProcessor
from datetime import datetime

class ChatbotCLI:
    """Command-line interface for the chatbot."""
    
    def __init__(self):
        """Initialize the CLI chatbot."""
        self.intent_matcher = IntentMatcher('data/intents.json')
        self.entity_extractor = EntityExtractor('data/entities.json')
        self.nlp_processor = NLPProcessor()
        self.conversation_history = []
    
    def print_welcome(self):
        """Print welcome message."""
        print("\n" + "="*60)
        print("     🤖 AI RULE-BASED CHATBOT 🤖")
        print("="*60)
        print("Welcome! I'm your AI assistant.")
        print("Type 'help' for commands, 'quit' to exit.")
        print("="*60 + "\n")
    
    def print_help(self):
        """Print help message."""
        print("\n" + "-"*60)
        print("AVAILABLE COMMANDS:")
        print("-"*60)
        print("  help         - Show this help message")
        print("  history      - Show conversation history")
        print("  clear        - Clear conversation history")
        print("  intents      - Show available intents")
        print("  quit/exit    - Exit the chatbot")
        print("-"*60 + "\n")
    
    def print_intents(self):
        """Print available intents."""
        print("\n" + "-"*60)
        print("AVAILABLE INTENTS:")
        print("-"*60)
        for intent in self.intent_matcher.intents:
            print(f"  • {intent['name']} (ID: {intent['id']})")
            print(f"    Patterns: {', '.join(intent['patterns'][:3])}...")
        print("-"*60 + "\n")
    
    def print_history(self):
        """Print conversation history."""
        if not self.conversation_history:
            print("\nNo conversation history yet.\n")
            return
        
        print("\n" + "-"*60)
        print("CONVERSATION HISTORY:")
        print("-"*60)
        for i, exchange in enumerate(self.conversation_history, 1):
            print(f"\n[{i}] User: {exchange['user_input']}")
            print(f"    Bot:  {exchange['bot_response']}")
            print(f"    Intent: {exchange['intent']} (Confidence: {exchange['confidence']:.2f})")
        print("-"*60 + "\n")
    
    def process_input(self, user_input: str):
        """Process user input and generate response."""
        # Handle commands
        if user_input.lower() == 'help':
            self.print_help()
            return
        elif user_input.lower() == 'history':
            self.print_history()
            return
        elif user_input.lower() == 'clear':
            self.conversation_history = []
            self.intent_matcher.clear_context()
            print("\n✓ History cleared.\n")
            return
        elif user_input.lower() == 'intents':
            self.print_intents()
            return
        elif user_input.lower() in ['quit', 'exit']:
            self.print_goodbye()
            sys.exit(0)
        
        # Process as chat message
        response_text, confidence, intent_id = self.intent_matcher.get_response(user_input)
        
        # Extract entities
        entities = self.entity_extractor.extract_entities(user_input)
        
        # Analyze sentiment
        sentiment = self.nlp_processor.detect_sentiment(user_input)
        
        # Store in history
        exchange = {
            'user_input': user_input,
            'bot_response': response_text,
            'intent': intent_id,
            'confidence': confidence,
            'timestamp': datetime.now().isoformat()
        }
        self.conversation_history.append(exchange)
        
        # Display response
        print(f"\nBot: {response_text}")
        print(f"    [Intent: {intent_id} | Confidence: {confidence:.2%}]")
        
        if entities:
            print(f"    [Entities: {', '.join([f'{k}: {v}' for k, v in entities.items()])}]")
        
        sentiment_label = max(sentiment, key=sentiment.get)
        print(f"    [Sentiment: {sentiment_label.upper()}]\n")
    
    def print_goodbye(self):
        """Print goodbye message."""
        print("\n" + "="*60)
        print("Thank you for chatting! Goodbye! 👋")
        print("="*60 + "\n")
    
    def run(self):
        """Run the CLI chatbot."""
        self.print_welcome()
        
        try:
            while True:
                try:
                    user_input = input("You: ").strip()
                    if user_input:
                        self.process_input(user_input)
                except EOFError:
                    self.print_goodbye()
                    break
        except KeyboardInterrupt:
            self.print_goodbye()

if __name__ == '__main__':
    cli = ChatbotCLI()
    cli.run()
