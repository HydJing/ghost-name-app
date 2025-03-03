import os
from flask import Flask
import logging
from routes.auth import auth_bp
from routes.phantom import phantom_bp

app = Flask(__name__)

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load config and models
from config import CLIENT_SECRETS, SCOPES, REDIRECT_URI
from models import GhostName, UserGhostName

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(phantom_bp)

if __name__ == "__main__":
    app.secret_key = os.urandom(24)  # Temporary; use Secret Manager in production
    app.run(host="0.0.0.0", port=8080, debug=True)