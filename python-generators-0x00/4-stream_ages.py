import mysql.connector

def stream_user_ages():
    """
    Generator that streams ages of users one by one.
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
        cursor = connection.cursor()
        cursor.execute("SELECT age FROM user_data")

        for (age,) in cursor:  # loop 1
            yield int(age)

    except mysql.connector.Error as err:
        print(f"❌ Database error: {err}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


def compute_average_age():
    """
    Compute average age using the generator without loading everything in memory.
    """
    total, count = 0, 0
    for age in stream_user_ages():  # loop 2
        total += age
        count += 1
    if count > 0:
        avg = total / count
        print(f"Average age of users: {avg:.2f}")
    else:
        print("No users found.")


if __name__ == "__main__":
    compute_average_age()
