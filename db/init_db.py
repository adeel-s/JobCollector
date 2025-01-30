import sqlite3
from supabase import create_client, Client
import sys, os

# Get the parent directory and add it to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import app_secrets as sec
sqliteSchemaFile = 'db\\sqlite_schema.sql'
supabaseSchemaFile = 'db\\supabase_schema.sql'
localDatabase = 'db\\database.db'
# Create a Supabase client

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