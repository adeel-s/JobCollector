import sqlite3, pandas, os, sys
from supabase import create_client, Client

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import app_secrets as sec
# Make this into a class at some point
sqliteSchemaFile = 'db\\sqlite_schema.sql'
supabaseSchemaFile = 'db\\supabase_schema.sql'
localDatabase = 'db\\database.db'
def writeDFSupabase(df, table):
    print("Connecting to Supabase...")
    try:
        supabase: Client = create_client(sec.SUPABASE_URL, sec.SUPABASE_KEY)
        print("Connected")
        data = df.to_dict(orient="records")
        print("Writing to the table...")
        response = supabase.table(table).upsert(data).execute()
        if len(response) < 200:
            print(response)
    except Exception as e:
        print("Supabase access failure: ", e)
    

def writeDFSqlite(df, table):
    print("Connecting to Sqlite...")
    try:
        connection = sqlite3.connect(localDatabase)
        print("Connected")
        print("Writing to the table...")
        df.to_sql(table, connection, if_exists="append", index=False)
        connection.commit()
        print("Done")
    except Exception as e:
        print("Sqlite access failure: ", e)
    finally:
        connection.close()
# this doesn't work right now
def initTables():
    supabase: Client = create_client(sec.SUPABASE_URL, sec.SUPABASE_KEY)
    connection = sqlite3.connect(localDatabase)

    with open(sqliteSchemaFile) as f:
        try:
            connection.executescript(f.read())
            connection.commit()
        except Exception as e:
            print(e)

    with open(supabaseSchemaFile) as f:
        try:
            response = supabase.rpc("pg_execute_sql", {"sql": f.read()}).execute()
            print(response)
        except Exception as e:
            print(e)  
    connection.close()