from flask import Flask, request, jsonify
from utils.api_key_generation import validate_api_key, store_api_key
import random

app = Flask(__name__)

# Middleware: Validate API Key
@app.before_request
def check_api_key():
    """Middleware to validate API key before processing any request."""
    if request.endpoint in ['random_text']:  # Restrict API access
        api_key = request.headers.get("X-API-KEY")

        if not api_key:
            return jsonify({"error": "API key required"}), 401

        if not validate_api_key(api_key):
            return jsonify({"error": "Invalid or expired API key"}), 403

# API Route: Random Text Generator
@app.route('/random-text', methods=['GET'])
def random_text():
    """Mock API that returns a random string of text."""
    words = ["flask", "api", "cloud", "random", "data", "testing", "validation"]
    return jsonify({"random_text": " ".join(random.choices(words, k=5))}), 200

# API Route: Generate API Key (For testing purposes)
@app.route('/generate-api-key', methods=['POST'])
def generate_api_key():
    """Generate and return a new API key."""
    user_email = request.json.get("email")
    if not user_email:
        return jsonify({"error": "Email required"}), 400

    api_key = store_api_key(user_email, session={})  # Store key without Flask session in testing
    return jsonify({"api_key": api_key}), 201

if __name__ == '__main__':
    app.run(debug=True, port=5002)  # Run API hub on port 5002
