from flask import Blueprint, render_template, request, redirect, url_for, session
from google.cloud import ndb
import random
import logging

phantom_bp = Blueprint("phantom", __name__)

logger = logging.getLogger(__name__)

from models import GhostName, UserGhostName
from utils import get_user

@phantom_bp.route("/")
def index():
    try:
        client = ndb.Client()
        with client.context():
            users = UserGhostName.query().fetch()
            user_email = get_user()
            link_text = "Change your current Phantom name" if user_email and any(u.email == user_email for u in users) else "Get a Phantom name"
        return render_template("index.html", users=users, link_text=link_text, logged_in=bool(user_email))
    except Exception as e:
        logger.error(f"Index route failed: {str(e)}")
        return "Datastore Error: Check server logs", 500

@phantom_bp.route("/phantom-form", methods=["GET", "POST"])
def phantom_form():
    if not get_user():
        return redirect(url_for("auth.login"))  
    if request.method == "POST":
        try:
            first_name = request.form["first_name"]
            last_name = request.form["last_name"]
            session["first_name"] = first_name
            session["last_name"] = last_name
            return redirect(url_for("phantom.phantom_results"))  # Updated from "phantom_results" to "phantom.phantom_results"
        except Exception as e:
            logger.error(f"Phantom form submission failed: {str(e)}")
            return "Form Error: Check server logs", 500
    return render_template("phantom_form.html")

@phantom_bp.route("/phantom-results", methods=["GET", "POST"])
def phantom_results():
    if not get_user():
        return redirect(url_for("auth.login"))  
    first_name = session.get("first_name")
    last_name = session.get("last_name")
    if not first_name or not last_name:
        return redirect(url_for("phantom.phantom_form"))  # Updated from "phantom_form" to "phantom.phantom_form"
    
    if request.method == "POST":
        try:
            selected_name = request.form["ghost_name"]
            ghost_part = selected_name.split("\"")[1]
            client = ndb.Client()
            with client.context():
                ghost = GhostName.query(GhostName.name == ghost_part).get()
                if ghost and not ghost.is_taken:
                    ghost.is_taken = True
                    ghost.put()
                user = UserGhostName.query(UserGhostName.email == get_user()).get()
                if not user:
                    user = UserGhostName(email=get_user())
                user.first_name = first_name
                user.last_name = last_name
                user.ghost_name = ghost_part
                user.put()
            return redirect(url_for("phantom.index"))  # Already correct
        except Exception as e:
            logger.error(f"Phantom results submission failed: {str(e)}")
            return "Selection Error: Check server logs", 500
    
    try:
        client = ndb.Client()
        with client.context():
            available = GhostName.query(GhostName.is_taken == False).fetch()
            if len(available) < 3:
                logger.warning("Not enough available ghost names.")
                return "Error: No available ghost names. Please contact the admin.", 500
            random.shuffle(available)
            options = [(f"{first_name} \"{ghost.name}\" {last_name}", ghost.description) for ghost in available[:3]]
        return render_template("phantom_results.html", options=options)
    except Exception as e:
        logger.error(f"Phantom results rendering failed: {str(e)}")
        return "Rendering Error: Check server logs", 500