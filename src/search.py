import json
from collections import defaultdict
from .config import USERS_FILE, TICKETS_FILE, ORGANIZATIONS_FILE

class ZendeskSearch:
    def __init__(self):
        #load data into data dict (in-memory)
        self.data = {
            "users": self.load_data(USERS_FILE, "users"),
            "tickets": self.load_data(TICKETS_FILE, "tickets"),
            "organizations": self.load_data(ORGANIZATIONS_FILE, "organizations")
        }

        #Create a list of allowed field needed for validation
        self.allowed_fields = {
            "users": sorted(self.data["users"][0].keys()) if self.data["users"] else [],
            "tickets": sorted(self.data["tickets"][0].keys()) if self.data["tickets"] else [],
            "organizations": sorted(self.data["organizations"][0].keys()) if self.data["organizations"] else []
        }

       # primary Indexes (for O(1) lookup using _id field)
        self.user_index = {}
        self.ticket_index = {}
        self.organization_index = {}

        # secondary Indexes (store only _ids list for references)
        self.users_by_org = defaultdict(list)
        self.tickets_by_org = defaultdict(list)
        self.tickets_by_user = defaultdict(list)
        self.tags_index = defaultdict(lambda: defaultdict(list))  # Multi-level dict for tags used for grouping

        self.build_indexes()

    def load_data(self, file_path, root_key):
        try:
            with open(file_path, "r") as f:
                data = json.load(f)
                return data.get(root_key, [])
        except (FileNotFoundError, json.JSONDecodeError):
            print(f"Warning: {file_path} not found or corrupted. Hence initializing empty data.")
            return []
    
    def build_indexes(self):
        """Function to build primary and secondary indexes for fast lookup"""
        for user in self.data["users"]:
            user_id = user["_id"]
            org_id = user.get("organization_id")

            # Store only primary index
            self.user_index[user_id] = user

            # Store only _id references in secondary indexes
            if org_id:
                self.users_by_org[org_id].append(user_id)

            for tag in user.get("tags", []):
                self.tags_index[tag]["users"].append(user_id)

        for ticket in self.data["tickets"]:
            ticket_id = ticket["_id"]
            org_id = ticket.get("organization_id")
            requester_id = ticket.get("requester_id")

            # Primary index
            self.ticket_index[ticket_id] = ticket

            # Secondary indexes store only _id references
            if org_id:
                self.tickets_by_org[org_id].append(ticket_id)
            if requester_id:
                self.tickets_by_user[requester_id].append(ticket_id)

            for tag in ticket.get("tags", []):
                self.tags_index[tag]["tickets"].append(ticket_id)

        for org in self.data["organizations"]:
            org_id = org["_id"]

            # Primary index
            self.organization_index[org_id] = org

            for tag in org.get("tags", []):
                self.tags_index[tag]["organizations"].append(org_id)

    def search(self, entity, field, value):
        """Perform search based on the given entity and field"""
        
        #serch for _id field with index
        if field == "_id":
            return self.search_by_id(entity, value)
        #search for tags on all 3 files/entity using tag index
        if field == "tags":
            return self.search_by_tag(value)

        #Search on non index fields mostly text fields with duplicate data
        results = []
        for entry in self.data[entity]:
            if str(entry.get(field, "")).lower() == value.lower():
                enriched_entry = {entity[:-1]: entry}  #key like "user", "ticket", "organization"
                
                if entity == "users":
                    enriched_entry["organization"] = self.organization_index.get(entry.get("organization_id"), {})
                    enriched_entry["tickets"] = [self.ticket_index[t] for t in self.tickets_by_user.get(entry["_id"], [])]
                elif entity == "tickets":
                    enriched_entry["organization"] = self.organization_index.get(entry.get("organization_id"), {})
                    enriched_entry["users"] = self.user_index.get(entry.get("requester_id"), {})
                elif entity == "organizations":
                    enriched_entry["users"] = [self.user_index[u] for u in self.users_by_org.get(entry["_id"], [])]
                    enriched_entry["tickets"] = [self.ticket_index[t] for t in self.tickets_by_org.get(entry["_id"], [])]
                
                results.append(enriched_entry)
        
        return results

    def search_by_id(self, entity, value):
        """Search using primary _id index + merge data from linked index"""
        result = None

        if entity == "users":
            result = self.user_index.get(value)
            if result:
                return {
                    "user": result,
                    "organization": self.organization_index.get(result.get("organization_id"), {}),
                    "tickets": [self.ticket_index[t] for t in self.tickets_by_user.get(value, [])],
                }

        elif entity == "tickets":
            result = self.ticket_index.get(value)
            if result:
                return {
                    "ticket": result,
                    "organization": self.organization_index.get(result.get("organization_id"), {}),
                    "users": self.user_index.get(result.get("requester_id"), {}),
                }

        elif entity == "organizations":
            result = self.organization_index.get(value)
            if result:
                return {
                    "organization": result,
                    "users": [self.user_index[u] for u in self.users_by_org.get(value, [])],
                    "tickets": [self.ticket_index[t] for t in self.tickets_by_org.get(value, [])],
                }

        return None

    def search_by_tag(self, value):
        """Search for documents by tag, fetching full records from primary indexes"""
        results = self.tags_index.get(value, {})

        return {
            "users": [self.user_index[u] for u in results.get("users", [])],
            "tickets": [self.ticket_index[t] for t in results.get("tickets", [])],
            "organizations": [self.organization_index[o] for o in results.get("organizations", [])],
        }

    def display_results(self, results):
        """Display results in a formatted and readable manner"""
        if not results:
            print("No results found.")
            return

        if isinstance(results, dict):
            for key, value in results.items():
                self.print_section(key, value)
        else: 
            for entry in results:
                for key, value in entry.items():
                    self.print_section(key, value)

    def print_section(self, title, data):
        """Helper to print each section in a readable format"""
        print(f"\n{title.capitalize()}:")
        print("-" * 40)
        
        if isinstance(data, list):
            if not data:
                print(f"  No {title.capitalize()} found.")
            else:
                for item in data:
                    self.print_entry(item)
                    print("-" * 40) 
        elif isinstance(data, dict):
            if not data:
                print(f"  No {title.capitalize()} found.")
            else:
                self.print_entry(data)
        else:
            print(f"  {data}")

    def print_entry(self, entry, indent=2):
        """Print a dictionary entry with formatted output"""
        if not isinstance(entry, dict):
            print(" " * indent + str(entry))
            return

        for key, value in entry.items():
            prefix = " " * indent
            if isinstance(value, list):
                print(f"{prefix}{key.capitalize()}:")
                if not value:
                    print(f"{prefix}  No {key.capitalize()} found.")
                else:
                    for item in value:
                        self.print_entry(item, indent + 4)
            else:
                print(f"{prefix}{key.capitalize()}: {value}")

    def is_valid_field(self, entity, field):
        """ Check if the given field is valid for the selected entity/type """
        return field in self.allowed_fields.get(entity, [])

    def show_help(self):
        """ Show allowed fields for all entity types """
        print("\nAllowed search fields:")
        for entity, fields in self.allowed_fields.items():
            print(f"\n{entity.capitalize()}: {', '.join(fields)}")
        print()


#uncomment below code for dev testing/debigging only

# if __name__ == "__main__":
#     search_tool = ZendeskSearch()

#     # Hardcoded values for test locally
#     entity = "users"  # values cab be "users", "tickets", or "organizations"
#     field = "name"  # field name to search 
#     value = "Andrew White"  # value to search for

#     # call search function
#     results = search_tool.search(entity, field, value)

#     #print the results
#     search_tool.display_results(results)