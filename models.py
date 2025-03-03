from google.cloud import ndb

class GhostName(ndb.Model):
    name = ndb.StringProperty()
    description = ndb.StringProperty()
    is_taken = ndb.BooleanProperty(default=False)

class UserGhostName(ndb.Model):
    email = ndb.StringProperty()
    first_name = ndb.StringProperty()
    last_name = ndb.StringProperty()
    ghost_name = ndb.StringProperty()