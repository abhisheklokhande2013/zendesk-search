import unittest
from src.search import ZendeskSearch

class TestSearch(unittest.TestCase):
    def setUp(self):
        self.search_tool = ZendeskSearch()
    
    # Test search by _id
    def test_search_user_by_id(self):
        result = self.search_tool.search("users", "_id", "92")
        #print("Search Result:", result)
        self.assertGreater(len(result), 0)
        self.assertEqual(result['user']['name'], "Teresa Hill")
        self.assertEqual(result['tickets'][0]['subject'], "Later here around here run future.")
    
    def test_search_ticket_by_id(self):
        result = self.search_tool.search("tickets", "_id", "ticket_399")
        #print("Search Result:", result)
        self.assertGreater(len(result), 0)
        self.assertEqual(result['ticket']['priority'], "P3")
        self.assertEqual(result['organization']['name'], "Reynolds, Rios and Andrews")
    
    def test_search_organization_by_id(self):
        result = self.search_tool.search("organizations", "_id", "34")
        #print("Search Result:", result)  # Keep for debugging
        self.assertIsNotNone(result.get("organization"), "No organization found in the result")
        self.assertEqual(result["organization"]["name"], "Hendrix Ltd")
    
    # test search by tags
    def test_search_user_by_tag(self):
        result = self.search_tool.search("users", "tags", "oil")
        #print("Search Result:", result)
        self.assertGreater(len(result["users"]), 0)
        self.assertEqual(result["users"][0]["name"], "Jason Davis")
        self.assertEqual(result["tickets"][0]["status"], "closed")
        self.assertEqual(len(result["organizations"]),0)
    
    def test_search_ticket_by_tag(self):
        result = self.search_tool.search("tickets", "tags", "oil")
        #print("Search Result:", result)        
        self.assertGreater(len(result["tickets"]), 0)
        ticket = result["tickets"][0] 
        self.assertEqual(ticket["_id"], "ticket_399")
    
    def test_search_organization_by_tag(self):
        result = self.search_tool.search("organizations", "tags", "oil")
        self.assertEqual(len(result), 3)
    
    # test search by non-indexed fields
    def test_search_user_by_name(self):
        result = self.search_tool.search("users", "name", "Jason Davis")
        #print("Search Result:", result)
        self.assertGreater(len(result), 0)
        self.assertTrue(any(entry["user"]["_id"] == "6" for entry in result))
        self.assertEqual(result[0]['organization']['domain'],"wallace.com")
    
    def test_search_user_by_email(self):
        result = self.search_tool.search("users", "email", "benjamingomez@example.org")
        #print("Search Result:", result)  
        self.assertGreater(len(result), 0)
        user = result[0]["user"]  
        self.assertEqual(user["_id"], "99")
    
    # Test search for empty values (finding tickets with no description)
    def test_serch_ticket_with_empty_description(self):
        result = self.search_tool.search("tickets", "description", "")
        #print("Search Result:", result)
        ticket = result[0]["ticket"] 
        self.assertEqual(ticket["description"], "")
    


if __name__ == "__main__":
    unittest.main()
