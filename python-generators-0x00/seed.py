import csv
import uuid
import mysql.connector
from mysql.connector import errorcode

# Connect to MySQL server
def connect_db():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",          # 🔑 change if needed
            password="password"   # 🔑 change if needed
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

# Create database ALX_prodev
def create_database(connection):
    cursor = connection.cursor()
    try:
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
        print("✅ Database ALX_prodev checked/created.")
    except mysql.connector.Error as err:
        print(f"❌ Failed creating database: {err}")
    finally:
        cursor.close()

# Connect directly to ALX_prodev
def connect_to_prodev():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",         
            password="password",
            database="ALX_prodev"
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None


# Create table if not exists
def create_table(connection):
    cursor = connection.cursor()
    create_table_query = """
    CREATE TABLE user_data (
        user_id CHAR(36) PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL,
        age DECIMAL(3,0) NOT NULL,
        INDEX (user_id)
    )
    """
    try:
        cursor.execute(create_table_query)
        print("Table user_data created.")
    except mysql.connector.Error as err:
        print(f" Error creating table: {err}")
    finally:
        cursor.close()

# Generator to read CSV file
def read_csv(file_path):
    try:
        with open(file_path, "r") as file:
            reader = csv.reader(file)
            next(reader)  # Skip header row
            for row in reader:
                yield row   # <-- generator yields rows lazily
    except FileNotFoundError:
        print("❌ user_data.csv not found.")
        return

# Insert data into user_data

def insert_data(connection, rows):
    cursor = connection.cursor()
    insert_query = """
    INSERT INTO user_data (user_id, name, email, age)
    VALUES (%s, %s, %s, %s)
    """
    try:
        for row in rows:   # <-- generator supplies rows one by one
            user_id = str(uuid.uuid4())  
            name, email, age = row
            # Check if email already exists
            cursor.execute("SELECT * FROM user_data WHERE email = %s", (email,))
            if not cursor.fetchone():
                cursor.execute(insert_query, (user_id, name, email, age))
        connection.commit()
        print("✅ Data inserted successfully.")
    except mysql.connector.Error as err:
        print(f"❌ Error inserting data: {err}")
    finally:
        cursor.close()

# Execution
if __name__ == "__main__":
    # Step 1: Connect to MySQL server
    server_conn = connect_db()
    if server_conn:
        create_database(server_conn)
        server_conn.close()

    # Step 2: Connect to ALX_prodev DB
    db_conn = connect_to_prodev()
    if db_conn:
        create_table(db_conn)

        # Step 3: Insert CSV data into DB using generator
        rows = read_csv("user_data.csv")
        if rows:
            insert_data(db_conn, rows)

        db_conn.close()
