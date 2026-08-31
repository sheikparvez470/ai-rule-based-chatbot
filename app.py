from flask import Flask, request, jsonify
from flask_cors import CORS
from utils.intent_matcher import IntentMatcher
from utils.entity_extractor import EntityExtractor
from utils.nlp_processor import NLPProcessor
import json
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)

# Initialize chatbot components
intent_matcher = IntentMatcher('data/intents.json')
entity_extractor = EntityExtractor('data/entities.json')
nlp_processor = NLPProcessor()

# Session storage for conversations
sessions = {}

@app.route('/', methods=['GET'])
def index():
    """Health check endpoint."""
    return jsonify({
        'status': 'running',
        'chatbot_name': 'AI Rule-Based Assistant',
        'version': '1.0.0',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/chat', methods=['POST'])
def chat():
    """
    Main chat endpoint.
    
    Request JSON format:
    {
        "user_message": "Hello!",
        "session_id": "optional_session_id"
    }
    """
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()
        session_id = data.get('session_id', 'default')
        
        if not user_message:
            return jsonify({'error': 'Message cannot be empty'}), 400
        
        # Process user input
        response_text, confidence, intent_id = intent_matcher.get_response(user_message)
        
        # Extract entities
        entities = entity_extractor.extract_entities(user_message)
        
        # Analyze sentiment
        sentiment = nlp_processor.detect_sentiment(user_message)
        
        # Check if it's a question
        is_question = nlp_processor.is_question(user_message)
        
        # Extract keywords
        keywords = nlp_processor.get_keywords(user_message, top_n=5)
        
        # Build response
        response = {
            'success': True,
            'message': response_text,
            'intent': intent_id,
            'confidence': round(confidence, 2),
            'entities': entities,
            'sentiment': {
                'positive': round(sentiment['positive'], 2),
                'negative': round(sentiment['negative'], 2),
                'neutral': round(sentiment['neutral'], 2)
            },
            'is_question': is_question,
            'keywords': keywords,
            'timestamp': datetime.now().isoformat()
        }
        
        # Store in session
        if session_id not in sessions:
            sessions[session_id] = []
        
        sessions[session_id].append({
            'user_message': user_message,
            'bot_response': response_text,
            'intent': intent_id,
            'confidence': confidence,
            'timestamp': datetime.now().isoformat()
        })
        
        return jsonify(response), 200
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/session/<session_id>', methods=['GET'])
def get_session(session_id):
    """Get conversation history for a session."""
    if session_id not in sessions:
        return jsonify({'error': 'Session not found'}), 404
    
    return jsonify({
        'session_id': session_id,
        'conversation': sessions[session_id]
    }), 200

@app.route('/api/session/<session_id>', methods=['DELETE'])
def delete_session(session_id):
    """Delete a session."""
    if session_id in sessions:
        del sessions[session_id]
        return jsonify({'message': 'Session deleted'}), 200
    return jsonify({'error': 'Session not found'}), 404

@app.route('/api/intents', methods=['GET'])
def get_intents():
    """Get all available intents."""
    intents = []
    for intent in intent_matcher.intents:
        intents.append({
            'id': intent['id'],
            'name': intent['name'],
            'patterns_count': len(intent['patterns']),
            'responses_count': len(intent['responses'])
        })
    return jsonify({'intents': intents}), 200

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint with detailed status."""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'intents_loaded': len(intent_matcher.intents),
        'active_sessions': len(sessions),
        'uptime': 'running'
    }), 200

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
