import json
import os
import random
from .config import USERS_FILE, TICKETS_FILE, ORGANIZATIONS_FILE, DATA_DIR
from faker import Faker

fake = Faker()

def generate_users(num=10):
    users = []
    for _ in range(num):
        user = {
            "_id": str(fake.random_int(min=1, max=100)),
            "url": fake.url(),
            "external_id": fake.uuid4(),
            "name": fake.name(),
            "alias": fake.first_name(),
            "created_at": fake.iso8601(),
            "active": str(fake.boolean()),
            "verified": str(fake.boolean()),
            "shared": str(fake.boolean()),
            "locale": fake.locale(),
            "timezone": fake.timezone(),
            "last_login_at": fake.iso8601(),
            "email": fake.email(),
            "phone": fake.phone_number(),
            "signature": fake.sentence(),
            "organization_id": str(fake.random_int(min=1, max=50)),
            "tags": [fake.word() for _ in range(4)],
            "suspended": str(fake.boolean()),
            "role": random.choice(["admin", "agent", "end-user"]),
        }
        users.append(user)
    return {"users": users}

def generate_tickets(num=10):
    tickets = []
    for _ in range(num):
        ticket = {
            "_id": "ticket_" + str(fake.random_int(min=1, max=1000)),
            "url": fake.url(),
            "external_id": fake.uuid4(),
            "created_at": fake.iso8601(),
            "type": random.choice(["support", "incident", "question"]),
            "subject": fake.sentence(),
            "description": fake.text(),
            "priority": random.choice(["P1", "P2", "P3"]),
            "status": random.choice(["open", "pending", "closed", "in progress"]),
            "recipient": fake.email(),
            "submitter_id": str(fake.random_int(min=1, max=100)),
            "assignee_id": str(fake.random_int(min=1, max=100)),
            "organization_id": str(fake.random_int(min=1, max=50)),
            "tags": [fake.word() for _ in range(3)],
            "has_incidents": str(fake.boolean()),
            "due_at": fake.iso8601(),
            "via": random.choice(["agent", "web", "chat"]),
            "requester_id": str(fake.random_int(min=1, max=100))
        }
        tickets.append(ticket)
    return {"tickets": tickets}

def generate_organizations(num=10):
    organizations = []
    for _ in range(num):
        organization = {
            "_id": str(fake.random_int(min=1, max=50)),
            "url": fake.url(),
            "external_id": fake.uuid4(),
            "name": fake.company(),
            "domain": fake.domain_name(),
            "names": fake.word(),
            "created_at": fake.iso8601(),
            "details": fake.sentence(),
            "shared_tickets": str(fake.random_int(min=1, max=5)),
            "tags": [fake.word() for _ in range(3)]
        }
        organizations.append(organization)
    return {"organizations": organizations}

def save_json(data, file_path):
    """Saves data to a JSON file."""
    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)

def generate_sample_data():
    """Generates sample data and saves it to JSON files."""
    os.makedirs(DATA_DIR, exist_ok=True)
    
    save_json(generate_users(), USERS_FILE)
    save_json(generate_tickets(), TICKETS_FILE)
    save_json(generate_organizations(), ORGANIZATIONS_FILE)

    print(f"Sample data generated in {DATA_DIR}")

#Run this file seperetly if data is missing
if __name__ == "__main__":
    generate_sample_data()
