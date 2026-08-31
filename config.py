import os
from datetime import datetime

# Flask Configuration
FLASK_DEBUG = os.getenv('FLASK_DEBUG', True)
FLASK_PORT = os.getenv('FLASK_PORT', 5000)

# Chatbot Configuration
CHATBOT_NAME = "AI Assistant"
DEFAULT_CONFIDENCE_THRESHOLD = 0.6
MAX_CONTEXT_HISTORY = 10
RESPONSE_TIMEOUT = 30

# Intent Configuration
INTENT_CATEGORIES = {
    "greeting": {"priority": 10, "weight": 1.0},
    "goodbye": {"priority": 10, "weight": 1.0},
    "help": {"priority": 8, "weight": 0.9},
    "faq": {"priority": 7, "weight": 0.8},
    "weather": {"priority": 6, "weight": 0.7},
    "time": {"priority": 6, "weight": 0.7},
    "general": {"priority": 1, "weight": 0.5},
}

# Logging
LOG_FILE = "chatbot.log"
LOG_LEVEL = "INFO"
