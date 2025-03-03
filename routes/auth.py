# Blueprint for authentication-related routes
from flask import Blueprint, redirect, url_for, request, session
from google_auth_oauthlib.flow import Flow
from google.oauth2 import id_token
from google.auth.transport import requests
import logging

# Define the auth blueprint
auth_bp = Blueprint("auth", __name__)

# Set up logging
logger = logging.getLogger(__name__)

# Import OAuth config and helper function
from config import CLIENT_SECRETS, SCOPES, REDIRECT_URI
from utils import get_user

@auth_bp.route("/login")
def login():
    """Redirect user to Google OAuth for authentication."""
    try:
        # Initialize OAuth flow
        flow = Flow.from_client_config(CLIENT_SECRETS, scopes=SCOPES)
        flow.redirect_uri = REDIRECT_URI
        # Generate authorization URL and state
        authorization_url, state = flow.authorization_url()
        session["state"] = state  # Store state for callback verification
        logger.info(f"Redirecting to OAuth URL: {authorization_url} with redirect_uri: {flow.redirect_uri}")
        return redirect(authorization_url)
    except Exception as e:
        logger.error(f"Login route failed: {str(e)}")
        return "OAuth Initiation Error: Check server logs", 500

@auth_bp.route("/callback")
def callback():
    """Handle Google OAuth callback and authenticate user."""
    try:
        # Initialize OAuth flow for token exchange
        flow = Flow.from_client_config(CLIENT_SECRETS, scopes=SCOPES)
        flow.redirect_uri = REDIRECT_URI
        logger.info(f"Fetching token with redirect_uri: {flow.redirect_uri}")
        logger.info(f"Authorization response: {request.url}")
        logger.info(f"Expected state: {session.get('state')}, Received state: {request.args.get('state')}")
        # Verify state to prevent CSRF
        if session.get("state") != request.args.get("state"):
            raise ValueError("State parameter mismatch")
        # Fetch token from Google
        flow.fetch_token(authorization_response=request.url)
        # Verify and extract user info from ID token
        id_info = id_token.verify_oauth2_token(flow.credentials.id_token, requests.Request(), CLIENT_SECRETS["web"]["client_id"])
        session["email"] = id_info["email"]  # Store user email in session
        logger.info(f"Login successful for email: {session['email']}")
        return redirect(url_for("phantom.index"))
    except Exception as e:
        logger.error(f"OAuth callback failed: {str(e)}")
        return f"OAuth Callback Error: {str(e)} - Check server logs", 500