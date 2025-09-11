import sqlite3
import functools
import time

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
    """
    A decorator that wraps a function inside a database transaction.
    If the function completes successfully, the transaction is committed.
    If an error occurs, the transaction is rolled back.
    """
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

def retry_on_failure(retries=3, delay=2):
    """
    A decorator factory that retries a function a specified number of times
    if it raises an exception, with a delay between retries.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            tries = 0
            while tries < retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    tries += 1
                    print(f"Attempt {tries} failed with error: {e}. Retrying in {delay} seconds...")
                    time.sleep(delay)
            print(f"All {retries} attempts failed. Giving up.")
            raise
        return wrapper
    return decorator

def cache_query(func):
    """
    A decorator that caches the results of a function based on its arguments
    to avoid redundant calls to the database.
    """
    cache = {}
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Create a hashable key from the function's arguments
        key = (func.__name__,) + args + tuple(sorted(kwargs.items()))
        
        if key in cache:
            print("Cache hit! Returning cached result.")
            return cache[key]
        
        print("Cache miss! Executing query...")
        result = func(*args, **kwargs)
        cache[key] = result
        return result
    return wrapper

# Note: The order of decorators matters.
# The inner decorator (@transactional) gets the connection first from the outer decorator (@with_db_connection).
@with_db_connection
@transactional
def update_user_email(conn, user_id, new_email):
    """
    Updates a user's email in the database.
    """
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id))

@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    """
    Fetches all users from the database.
    """
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()

@with_db_connection
@cache_query
def get_user_by_id_cached(conn, user_id):
    """
    Fetches a user by ID and caches the result.
    """
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    return cursor.fetchone()

# Example usage to create a dummy database with an email column
def setup_database():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT
        )
    ''')
    cursor.execute("INSERT OR IGNORE INTO users (id, name, email) VALUES (1, 'Alice', 'alice@example.com')")
    cursor.execute("INSERT OR IGNORE INTO users (id, name, email) VALUES (2, 'Bob', 'bob@example.com')")
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

print("Initial email for user ID 1:", get_user_email(1))

# Update user's email with automatic transaction handling
print("\nAttempting to update user 1's email...")
try:
    update_user_email(user_id=1, new_email='Crawford_Cartwright@hotmail.com')
    print("Update successful.")
except sqlite3.Error as e:
    print(f"Update failed with error: {e}")

print("Current email for user ID 1:", get_user_email(1))

# attempt to fetch users with automatic retry on failure
print("\nAttempting to fetch users...")
try:
    users = fetch_users_with_retry()
    print("Fetched users successfully:")
    for user in users:
        print(user)
except Exception as e:
    print(f"Could not fetch users after multiple retries: {e}")

# Demonstrate the caching decorator
print("\nAttempting to fetch user 1 multiple times with caching...")
user_1_a = get_user_by_id_cached(user_id=1)
print(f"First fetch result: {user_1_a}")
user_1_b = get_user_by_id_cached(user_id=1)
print(f"Second fetch result: {user_1_b}")

print("\nAttempting to fetch a different user (ID 2)...")
user_2 = get_user_by_id_cached(user_id=2)
print(f"Third fetch result (different user): {user_2}")

print("\nAttempting to fetch user 1 one more time...")
user_1_c = get_user_by_id_cached(user_id=1)
print(f"Fourth fetch result: {user_1_c}")
