# Datastore models for ghost names and user assignments
from google.cloud import ndb

class GhostName(ndb.Model):
    """Model for available ghost names in Datastore."""
    name = ndb.StringProperty()  # Ghost name (e.g., "Bogle")
    description = ndb.StringProperty()  # Description (e.g., "A mischievous spirit")
    is_taken = ndb.BooleanProperty(default=False)  # Whether the name is assigned

class UserGhostName(ndb.Model):
    """Model for user-assigned ghost names in Datastore."""
    email = ndb.StringProperty()  # User's email from Google OAuth
    first_name = ndb.StringProperty()  # User's entered first name
    last_name = ndb.StringProperty()  # User's entered last name
    ghost_name = ndb.StringProperty()  # Assigned ghost name