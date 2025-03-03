# Main entry point for the Flask application
from flask import Flask
import os
import logging
from routes.auth import auth_bp
from routes.phantom import phantom_bp

# Initialize Flask app
app = Flask(__name__)

# Configure logging for debugging and error tracking
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Register blueprints for modular routing
app.register_blueprint(auth_bp)  # Authentication routes
app.register_blueprint(phantom_bp)  # Phantom name routes

# Entry point for local testing
if __name__ == "__main__":
    app.secret_key = os.urandom(24)  # Temporary secret key for session management
    app.run(host="0.0.0.0", port=8080, debug=True)  # Run Flask app locally