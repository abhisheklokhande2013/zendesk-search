import os

# This is base directory for data files
DATA_DIR = os.getenv("DATA_DIR", "./data")

# Paths to the JSON data files
USERS_FILE = os.path.join(DATA_DIR, "users.json")
TICKETS_FILE = os.path.join(DATA_DIR, "tickets.json")
ORGANIZATIONS_FILE = os.path.join(DATA_DIR, "organizations.json")