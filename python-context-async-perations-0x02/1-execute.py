import sqlite3

class DatabaseConnection:
    """
    A context manager to handle database connections automatically.
    The connection is opened upon entering the context and closed
    upon exiting, regardless of whether a commit or rollback is needed.
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

class ExecuteQuery:
    """
    A context manager to execute a single query and return the results.
    It handles opening and closing the database connection.
    """
    def __init__(self, db_name, query, params=()):
        self.db_name = db_name
        self.query = query
        self.params = params
        self.conn = None
        self.cursor = None

    def __enter__(self):
        """
        Establishes a connection, executes the query, and returns the cursor.
        """
        try:
            self.conn = sqlite3.connect(self.db_name)
            self.cursor = self.conn.cursor()
            print(f"Executing query: {self.query} with parameters: {self.params}")
            self.cursor.execute(self.query, self.params)
            return self.cursor
        except sqlite3.Error as e:
            print(f"Error executing query: {e}")
            self.conn.close()
            self.conn = None
            self.cursor = None
            raise

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Closes the cursor and the database connection.
        """
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
            print("Database connection closed.")
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
            name TEXT NOT NULL,
            age INTEGER
        )
    ''')
    cursor.execute("INSERT OR IGNORE INTO users (id, name, age) VALUES (1, 'Alice', 22)")
    cursor.execute("INSERT OR IGNORE INTO users (id, name, age) VALUES (2, 'Bob', 30)")
    cursor.execute("INSERT OR IGNORE INTO users (id, name, age) VALUES (3, 'Charlie', 28)")
    conn.commit()
    conn.close()

if __name__ == "__main__":
    # Set up the database before running the main logic
    setup_database()
    
    # Example using the DatabaseConnection context manager
    print("Using the DatabaseConnection context manager:")
    try:
        with DatabaseConnection('users.db') as conn:
            cursor = conn.cursor()
            print("\nExecuting query: SELECT * FROM users")
            cursor.execute("SELECT * FROM users")
            
            results = cursor.fetchall()
            print("Query Results:")
            for row in results:
                print(row)
                
    except sqlite3.Error as e:
        print(f"\nAn error occurred during query execution: {e}")
    
    # Example using the new ExecuteQuery context manager
    print("\n" + "="*40)
    print("Using the ExecuteQuery context manager:")
    try:
        with ExecuteQuery('users.db', "SELECT * FROM users WHERE age > ?", (25,)) as cursor:
            results = cursor.fetchall()
            print("\nQuery Results for users older than 25:")
            for row in results:
                print(row)
    except sqlite3.Error as e:
        print(f"\nAn error occurred during query execution: {e}")

    print("\nScript finished.")
