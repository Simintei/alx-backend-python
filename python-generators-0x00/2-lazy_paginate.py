import mysql.connector

def paginate_users(page_size, offset):
    """
    Fetch a single page of users from the database.
    """
    connection = None
    cursor = None
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",          # 🔑 update as needed
            password="password",  # 🔑 update as needed
            database="ALX_prodev"
        )
        cursor = connection.cursor(dictionary=True)
        cursor.execute(
            "SELECT * FROM user_data LIMIT %s OFFSET %s",
            (page_size, offset)
        )
        rows = cursor.fetchall()
        return rows
    except mysql.connector.Error as err:
        print(f"❌ Database error: {err}")
        return []
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


def lazy_paginate(page_size):
    """
    Generator that lazily fetches pages of data from the DB.
    Only one loop is used.
    """
    offset = 0
    while True:  # <-- only one loop
        page = paginate_users(page_size, offset)
        if not page:
            break
        yield page
        offset += page_size
