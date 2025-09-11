import sqlite3

class DatabaseConnection:
    """
    A context manager to handle database connections automatically.
    The connection is opened upon entering the context and closed
    upon exiting, regardless of whether an error occurred.
    """
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None

    def __enter__(self):
        """
        Connects to the database and returns the connection object.
        """
        try:
            self.conn = sqlite3.connect(self.db_name)
            print(f"Successfully connected to the database: {self.db_name}")
            return self.conn
        except sqlite3.Error as e:
            print(f"Error connecting to database: {e}")
            self.conn = None  # Ensure conn is None on failure
            raise  # Re-raise the exception

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Closes the database connection.
        This method is called automatically upon exiting the 'with' block.
        """
        if self.conn:
            self.conn.close()
            print("Database connection closed.")
        # Returning False here will allow any exception to be re-raised
        return False

# --- Example Usage ---

def setup_database():
    """
    Creates a dummy database and a 'users' table for demonstration.
    """
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

# Set up the database before running the main logic
setup_database()

print("Using the DatabaseConnection context manager:")

try:
    # The 'with' statement handles the __enter__ and __exit__ calls for you
    with DatabaseConnection('users.db') as conn:
        cursor = conn.cursor()
        print("\nExecuting query: SELECT * FROM users")
        cursor.execute("SELECT * FROM users")
        
        # Fetch and print the results
        results = cursor.fetchall()
        print("Query Results:")
        for row in results:
            print(row)
            
except sqlite3.Error as e:
    print(f"\nAn error occurred during query execution: {e}")

print("\nScript finished.")

