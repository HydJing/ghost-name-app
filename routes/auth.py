from flask import Blueprint, redirect, url_for, request, session
from google_auth_oauthlib.flow import Flow
from google.oauth2 import id_token
from google.auth.transport import requests
import logging

auth_bp = Blueprint("auth", __name__)

logger = logging.getLogger(__name__)

from config import CLIENT_SECRETS, SCOPES, REDIRECT_URI
from utils import get_user

@auth_bp.route("/login")
def login():
    try:
        flow = Flow.from_client_config(CLIENT_SECRETS, scopes=SCOPES)
        flow.redirect_uri = REDIRECT_URI
        authorization_url, state = flow.authorization_url()
        session["state"] = state
        logger.info(f"Redirecting to OAuth URL: {authorization_url} with redirect_uri: {flow.redirect_uri}")
        return redirect(authorization_url)
    except Exception as e:
        logger.error(f"Login route failed: {str(e)}")
        return "OAuth Initiation Error: Check server logs", 500

@auth_bp.route("/callback")
def callback():
    try:
        flow = Flow.from_client_config(CLIENT_SECRETS, scopes=SCOPES)
        flow.redirect_uri = REDIRECT_URI
        logger.info(f"Fetching token with redirect_uri: {flow.redirect_uri}")
        logger.info(f"Authorization response: {request.url}")
        logger.info(f"Expected state: {session.get('state')}, Received state: {request.args.get('state')}")
        if session.get("state") != request.args.get("state"):
            raise ValueError("State parameter mismatch")
        flow.fetch_token(authorization_response=request.url)
        id_info = id_token.verify_oauth2_token(flow.credentials.id_token, requests.Request(), CLIENT_SECRETS["web"]["client_id"])
        session["email"] = id_info["email"]
        logger.info(f"Login successful for email: {session['email']}")
        return redirect(url_for("phantom.index"))  # Already correct
    except Exception as e:
        logger.error(f"OAuth callback failed: {str(e)}")
        return f"OAuth Callback Error: {str(e)} - Check server logs", 500