"""
Write a Python script that connects to a SQLite database, creates a table if it doesn’t exist, inserts some records, and queries the table to retrieve all records.
"""

import sqlite3


def setup_db():
    conn = sqlite3.connect(":memory:")  # use an in-memory database for testing
    cursor = conn.cursor()
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS users(
                            id INTEGER PRIMARY KEY,
                            name TEXT,
                            age INTEGER)
                    """
    )

    cursor.execute("INSERT INTO users (name, age) VALUES (?, ?)", ("Alice", 30))
    cursor.execute("INSERT INTO users (name, age) VALUES (?, ?)", ("Bob", 27))
    conn.commit()
    return conn


def query_db(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()


conn = setup_db()
records = query_db(conn)
print(records)
conn.close()
