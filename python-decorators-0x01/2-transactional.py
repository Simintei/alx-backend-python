import sqlite3
import functools

def with_db_connection(func):
    """
    A decorator that handles database connection, passing it to the decorated
    function and ensuring it's closed afterward.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = None
        try:
            # Open the database connection
            conn = sqlite3.connect('users.db')
            
            # Pass the connection object as the first argument
            return func(conn, *args, **kwargs)
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return None
        finally:
            # Ensure the connection is closed, even if an error occurred
            if conn:
                conn.close()
    return wrapper

def transactional(func):
   @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        try:
            # The database connection is expected as the first argument
            result = func(conn, *args, **kwargs)
            conn.commit()
            print("Transaction committed.")
            return result
        except sqlite3.Error as e:
            print(f"Transaction failed due to error: {e}")
            conn.rollback()
            print("Transaction rolled back.")
            raise  # Re-raise the exception to propagate the error
    return wrapper
  #inner decorator(@transactional) gets the connection from the outer decorator (@with_db_connection)
@with_db_connection
@transactional
def update_user_email(conn, user_id, new_email): 
  #updates a users email in the database
cursor = conn.cursor() 
cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id)) 

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

# Helper function to check the current email in the database
def get_user_email(user_id):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("SELECT email FROM users WHERE id = ?", (user_id,))
    email = cursor.fetchone()
    conn.close()
    return email[0] if email else None
  
# Set up the database
setup_database()

# Fetch user by ID with automatic connection handling
print("Attempting to fetch user with ID 1...")
user = get_user_by_id(user_id=1)
if user:
    print("User found:", user)
else:
    print("User not found.")

print("\nAttempting to fetch user with a non-existent ID 3...")
user = get_user_by_id(user_id=3)
if user:
    print("User found:", user)
else:
    print("User not found.")
