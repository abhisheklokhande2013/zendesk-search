from .search import ZendeskSearch
from .config import DATA_DIR
from .utils import print_logo
import os

def main():
    #Show application ASCII logo on console    
    print("#" * 100)
    print_logo()

    #Ensure data directory exists
    os.makedirs(DATA_DIR, exist_ok=True)

    search_tool = ZendeskSearch()
    
    while True:
        #User prompt screen for user input
        print("#" * 100)
        print("\n  Select search-by option:\n")
        print("      1) Users")
        print("      2) Tickets")
        print("      3) Organizations")
        print("      4) Help")
        print("\n  Type 'quit' to exit")
        
        entity = input("\nEnter your choice: ").strip()
        
        if entity == 'quit':
            break

        entity_map = {"1": "users", "2": "tickets", "3": "organizations"}
        
        if entity == "4":
            search_tool.show_help()
            continue

        entity = entity_map.get(entity)
        if not entity:
            print("\nInvalid selection. Try again.")
            continue

        field = input("Enter search field: ").strip()
        if not search_tool.is_valid_field(entity, field):
            print(f"\nError: '{field}' is not a valid search term/field for {entity}. Use 'Help' to see valid fields for all type\n")
            continue  

        value = input("Enter search value: ").strip()
        print("\nOutput:\n")
        #perform search and show result
        results = search_tool.search(entity, field, value) or []
        search_tool.display_results(results)
   
#entry point main funciton
if __name__ == "__main__":
    main()
