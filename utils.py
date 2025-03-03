from flask import session

def get_user():
    return session.get("email")