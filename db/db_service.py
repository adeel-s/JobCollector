import sqlite3, pandas, os, sys, json
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
        print("Writing to table %s ..." %table)
        response = supabase.table(table).upsert(data).execute()
    except Exception as e:
        print("Supabase access failure: ", e)
    

def writeDFSqlite(df, table):
    print("Connecting to Sqlite...")
    try:
        connection = sqlite3.connect(localDatabase)
        print("Connected")
        print("Writing to table %s ..." %table)
        df.to_sql(table, connection, if_exists="append", index=False)
        connection.commit()
        print("Done")
    except Exception as e:
        print("Sqlite access failure: ", e)
    finally:
        connection.close()
def getJobs():
    print("Connecting to Supabase...")
    try:
        supabase: Client = create_client(sec.SUPABASE_URL, sec.SUPABASE_KEY)
        print("Connected")
        response = supabase.table("jobs").select("*").execute()
    except Exception as e:
        print("Supabase access failure: ", e)
    return response.data

def backupSupabase():
    print("BackupSupabase stub")

def getIDs(IDBatchSize):
    print("Connecting to Supabase...")
    try:
        supabase: Client = create_client(sec.SUPABASE_URL, sec.SUPABASE_KEY)
        print("Connected")
        response = supabase.table("job_ids").select("l_id").eq("processed", False).limit(IDBatchSize).execute()
    except Exception as e:
        print("Supabase access failure: ", e)
    return response.data

def updateJobIDs(jobs):
    print("Connecting to Supabase...")
    try:
        supabase: Client = create_client(sec.SUPABASE_URL, sec.SUPABASE_KEY)
        print("Connected")
        
        print("Marking job ids as processed")
        for i, row in jobs.iterrows():
            response = (supabase.table("job_ids").update({"processed": True}).eq("l_id", row["l_id"]).execute())
    except Exception as e:
        print("Supabase update failure: ", e)