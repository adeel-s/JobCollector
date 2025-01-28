import sqlite3

connection = sqlite3.connect('database.db')


with open('schema.sql') as f:
    try:
        connection.executescript(f.read())
    except Exception as e:
        print(e)


cur = connection.cursor()

cur.execute("INSERT INTO posts (title, content) VALUES (?, ?)",
            ('First Post', 'Content for the first post')
            )

cur.execute("INSERT INTO posts (title, content) VALUES (?, ?)",
            ('Second Post', 'Content for the second post')
            )

connection.commit()
connection.close()