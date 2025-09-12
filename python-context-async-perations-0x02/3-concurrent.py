import asyncio
import aiosqlite
import sqlite3
import os

async def async_fetch_users():
    """
    Asynchronous function to fetch all users from the database.
    """
    # Using async with for aiosqlite handles connection opening and closing
    async with aiosqlite.connect("users.db") as db:
        async with db.execute("SELECT * FROM users") as cursor:
            users = await cursor.fetchall()
            print("Finished fetching all users.")
            return users

async def async_fetch_older_users():
    """
    Asynchronous function to fetch users older than 40.
    """
    async with aiosqlite.connect("users.db") as db:
        async with db.execute("SELECT * FROM users WHERE age > ?", (40,)) as cursor:
            older_users = await cursor.fetchall()
            print("Finished fetching older users.")
            return older_users

async def fetch_concurrently():
    """
    Runs both asynchronous fetch functions concurrently using asyncio.gather.
    """
    # Create two tasks to run the queries concurrently
    task1 = asyncio.create_task(async_fetch_users())
    task2 = asyncio.create_task(async_fetch_older_users())
    
    # asyncio.gather runs the tasks and waits for them to complete.
    # The results are returned in the order of the tasks.
    all_users, older_users = await asyncio.gather(task1, task2)
    
    print("\n--- Concurrently Fetched Results ---")
    print("All Users:", all_users)
    print("Older Users:", older_users)
    print("--------------------------------------")


def setup_database():
    """
    Synchronous function to set up the database for the example.
    This runs once before the asyncio event loop starts.
    """
    if os.path.exists("users.db"):
        os.remove("users.db")
        print("Existing database removed.")

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            age INTEGER
        )
    ''')
    cursor.execute("INSERT INTO users (name, age) VALUES ('Alice', 22)")
    cursor.execute("INSERT INTO users (name, age) VALUES ('Bob', 30)")
    cursor.execute("INSERT INTO users (name, age) VALUES ('Charlie', 28)")
    cursor.execute("INSERT INTO users (name, age) VALUES ('Diana', 45)")
    cursor.execute("INSERT INTO users (name, age) VALUES ('Eve', 50)")
    conn.commit()
    conn.close()
    print("Database setup complete.")


if __name__ == "__main__":
    setup_database()
    # The asyncio.run() function executes the main coroutine until it completes.
    asyncio.run(fetch_concurrently())
