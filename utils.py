# Utility functions for the application
from flask import session

def get_user():
    """Retrieve the authenticated user's email from the session."""
    return session.get("email")