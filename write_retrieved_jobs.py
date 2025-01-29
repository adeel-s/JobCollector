import sqlite3
import pandas

# Should I parameterize DB writing?

def dbWrite(tableName, df, cols):

    print("Connecting to the database")
    try:
        connection = sqlite3.connect('database.db')
        print("Connected to the database")
        print("Writing to the database")
        df.to_sql('jobs', connection, if_exists='append', index=False)


        connection.commit()

    except Exception as e:
        print("Error while writing to database:", e)
    finally:
        connection.close()
    print("Updated database, closed connection")

# tableName = "jobs"
# cols = ["company", "title", "location", "description"]
# query = "INSERT OR IGNORE INTO " + tableName + " ("
# placeholders = "?, " * len(cols)
# for col in cols:
#     query += col + ", "
# query = query[0:len(query)-2] + ") VALUES (" + "?, " * (len(cols) - 1) + "?)"

# print(query)
