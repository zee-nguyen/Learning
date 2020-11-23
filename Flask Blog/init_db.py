import sqlite3

# open a connection to a database file
connection = sqlite3.connect('database.db')

with open('schema.sql') as f:
    # executes multiple SQL statements at once
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO posts (title, content) VALUES (?, ?)",
            ('First Post', 'Content for the first post')
            )

cur.execute("INSERT INTO posts (title, content) VALUES (?, ?)",
            ('Second Post', 'Content for the second post')
            )

connection.commit()
connection.close()
