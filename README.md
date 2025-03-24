# Zendesk Search Appication
 
## Overview
Zendesk Search is a command-line application that allows users to search through users, tickets, and organizations. It provides a fast lookup with indexed search.

## Assumptions & Indexing Strategy
1. Data Availability
- All three data files (users.json, tickets.json, organizations.json) must be present in the data folder before starting the application.
- If any file is missing, it must be manually created or generated using the data_generator.py utility.

2. Data Loading & Indexing
- When the application starts, it loads the data into memory and builds necessary indexes for efficient lookup operations.
- The indexes significantly improve search performance, especially for frequently queried fields.
- Some low-priority fields (e.g., name, created_at) are not indexed, as they are assumed to be less frequently searched.

3. Indexed Fields & Lookup Optimization
- Primary Indexes:
   - _id (for fast retrieval of unique records)
   - tags (for searching entities based on tags)

- Linked Indexes:
   - organization_id (for linking users and tickets to organizations)
   - requester_id (for fetching tickets requested by a user)

4. Search Time Complexity
- With Indexing:
   O(1) to O(log N) (Hash Map / Dictionary-based lookups for indexed fields)

- Without Indexing:
   O(N) (Linear search required for non-indexed fields like name, created_at)

5. Trade-offs in Indexing
- Indexing speeds up searches but increases memory usage.
- Fields with a high probability of lookups are indexed, while rarely searched fields remain unindexed to conserve memory.

6. Summary
 - The application ensures efficient lookups through selective indexing while maintaining a balance between speed and memory consumption. - Users searching non-indexed fields should expect slower response times compared to indexed fields.

## Features
- Search through users, tickets, and organizations
- Supports searcy by any field, including tags
- Generates sample data if missing (manual step given in doc) 
- Simple command-line interface

## Prerequisites
- Python 3.8+ required
- `pip` installed (Python package manager)

## Install Dependencies
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/zendesk-search-cli.git
   cd zendesk-search
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
Run the application using:
```bash
./run.sh
```
or manually start with:
```bash
python -m src.main
```

## Example Queries
1. Start the application:
   ```
    Select search-by option:

      1) Users
      2) Tickets
      3) Organizations
      4) Help

    Type 'quit' to exit
   ```

2. Search by `_id` for Users data:
   ```
   Enter your choice: 1

   Enter search field: _id
   Enter search value: 6

   Output:

   User:
   ----------------------------------------
   _id: 6
   Url: http://thompson-walker.org/
   External_id: 68ede15a-ed21-4354-85b3-9432902621da
   Name: Jason Davis
   Alias: Timothy
   Created_at: 1996-02-27T17:52:42
   Active: True
   Verified: True
   Shared: False
   Locale: ps_AF
   Timezone: America/Port_of_Spain
   Last_login_at: 2003-09-04T22:36:01
   Email: bradfordsamuel@example.net
   Phone: 648-366-0888x757
   Signature: House them worker ever expect Democrat.
   Organization_id: 34
   Tags:
         increase
         various
         oil
         wide
   Suspended: True
   Role: admin

   Organization:
   ----------------------------------------
   _id: 34
   Url: https://www.richard.com/
   External_id: f72490e1-fb66-446e-805c-486b0899e946
   Name: Hendrix Ltd
   Domain: wallace.com
   Names: service
   Created_at: 1973-11-18T22:37:06
   Details: This almost before it.
   Shared_tickets: 4
   Tags:
         heavy
         anything
         something

   Tickets:
   ----------------------------------------
   No Tickets found.
   ```

## Project Structure
```
zendesk_search/
|── data/                     # JSON data files (pre-req for project to start)
|── src/                      # Source code
|   ├── main.py               # Entry point for CLI
|   ├── search.py             # Search functionality
|   ├── data_generator.py     # Generates sample data manually
|   ├── config.py             # Configuration settings
|   ├── utils.py              # Utility functions
|── tests/                    # Unit tests
|── README.md                 # Project documentation
|── requirements.txt          # Python dependencies
|── run.sh                    # Shell script to run the app
```

## Manually generate input JSON files (only if missing from .data folder)
1. Go to zendesk_search/ 
2. Run below command to generate users.json, tickets.json and orginizations.json
```bash
python -m src.data_generator
```

## Running Tests
Run unit tests using:
```bash
python -m unittest tests.test_search
```
