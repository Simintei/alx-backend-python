import mysql.connector

def stream_users():
    connection = None
    cursor = None
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",          # 🔑 update as needed
            password="password",  # 🔑 update as needed
            database="ALX_prodev"
        )
        cursor = connection.cursor(dictionary=True)  # return rows as dicts
        cursor.execute("SELECT * FROM user_data")

        for row in cursor:   # <-- only one loop
            yield row

    except mysql.connector.Error as err:
        print(f"❌ Database error: {err}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
