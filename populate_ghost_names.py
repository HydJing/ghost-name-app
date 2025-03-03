import csv
from google.cloud import ndb

class GhostName(ndb.Model):
    name = ndb.StringProperty()
    description = ndb.StringProperty()
    is_taken = ndb.BooleanProperty(default=False)

def populate_ghost_names(csv_file="ghost_names.csv"):
    client = ndb.Client()
    with client.context():
        existing = {g.name for g in GhostName.query().fetch()}
        with open(csv_file, "r", encoding="utf-8") as f:  # Explicitly use UTF-8
            reader = csv.DictReader(f)
            for row in reader:
                name = row["Ghost name"]
                if name not in existing:
                    ghost = GhostName(
                        name=name,
                        description=row["Description"]
                    )
                    ghost.put()
        print(f"Populated ghost names from {csv_file} into Datastore.")

if __name__ == "__main__":
    populate_ghost_names()