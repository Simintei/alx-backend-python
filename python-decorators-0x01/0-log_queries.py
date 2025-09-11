import sqlite3
import functools
from datetime import datetime

#### decorator to log SQL queries
def log_queries(func):
    """
    A decorator that logs the SQL query being passed to the decorated function.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Check if a 'query' keyword argument exists in the function call.
        query = kwargs.get('query')
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if query:
            print(f"[{current_time}] Executing SQL query: {query}")
        else:
            print(f"[{current_time}] No SQL query found to log.")
        
        # Call the original function with its arguments and return its result.
        return func(*args, **kwargs)
    return wrapper

@log_queries
def fetch_all_users(query):
    """
    Connects to an SQLite database, executes a query, and fetches results.
    """
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

# Example usage to create a dummy database and table for testing the decorator
def setup_database():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL
        )
    ''')
    cursor.execute("INSERT OR IGNORE INTO users (id, name) VALUES (1, 'Alice')")
    cursor.execute("INSERT OR IGNORE INTO users (id, name) VALUES (2, 'Bob')")
    conn.commit()
    conn.close()

# Set up the database
setup_database()

# Fetch users while logging the query using the decorator
users = fetch_all_users(query="SELECT * FROM users")

# Print the fetched users to verify the function worked
print("\nFetched users:")
for user in users:
    print(user)
