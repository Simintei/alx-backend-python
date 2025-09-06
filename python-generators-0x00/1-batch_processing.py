import mysql.connector

def stream_users_in_batches(batch_size):
    """
    Generator that streams rows in batches from user_data table.
    """
    connection = None
    cursor = None
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",          
            password="password",  
            database="ALX_prodev"
        )
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user_data")

        while True:  # loop 1
            batch = cursor.fetchmany(batch_size)
            if not batch:
                break
            yield batch   # yield the whole batch

    except mysql.connector.Error as err:
        print(f"❌ Database error: {err}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


def batch_processing(batch_size):
    """
    Processes batches and yields users over age 25.
    """
    for batch in stream_users_in_batches(batch_size):  # loop 2
        filtered = [row for row in batch if int(row["age"]) > 25]  # loop 3 (list comprehension)
        yield filtered
