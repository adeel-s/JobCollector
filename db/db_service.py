import sqlite3, pandas as pd, os, sys, json
from supabase import create_client, Client

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

dbJobs = []

import app_secrets as sec
# Make this into a class at some point
sqliteSchemaFile = 'db\\sqlite_schema.sql'
supabaseSchemaFile = 'db\\supabase_schema.sql'
localDatabase = 'db\\database.db'
jobsTable = "jobs"
idsTable = "job_ids"

def writeDFSupabase(df, table):
    print("Connecting to Supabase...")
    try:
        supabase: Client = create_client(sec.SUPABASE_URL, sec.SUPABASE_KEY)
        print("Connected")
        data = df.to_dict(orient="records")
        print("Writing to table %s ..." %table)
        response = supabase.table(table).upsert(data, on_conflict=["l_id"], ignore_duplicates=True).execute()
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

def getAllJobs():
    print("Connecting to Supabase...")
    try:
        supabase: Client = create_client(sec.SUPABASE_URL, sec.SUPABASE_KEY)
        print("Connected")
        response = supabase.table(jobsTable).select("*").execute()
    except Exception as e:
        print("Supabase access failure: ", e)
    return response.data

def getNewJobs():
    print("Connecting to Supabase...")
    try:
        supabase: Client = create_client(sec.SUPABASE_URL, sec.SUPABASE_KEY)
        print("Connected")
        # COULD ADD SAVED TO THIS↓
        response = supabase.table(jobsTable).select("*").\
            eq("applied", False).eq("rejected", False).eq("not_interested", False).execute()
    except Exception as e:
        print("Supabase access failure: ", e)
    return response.data

def getAllIDs():
    print("Connecting to Supabase...")
    try:
        supabase: Client = create_client(sec.SUPABASE_URL, sec.SUPABASE_KEY)
        print("Connected")
        response = supabase.table(idsTable).select("*").execute()
    except Exception as e:
        print("Supabase access failure: ", e)
    return response.data

def backupSupabase():
    print("Backing up Supabase to Sqlite")
    jobsDF = pd.DataFrame(getAllJobs())
    idsDF = pd.DataFrame(getAllIDs())
    writeDFSqlite(jobsDF, jobsTable)
    writeDFSqlite(idsDF, idsTable)

def getIDs(IDBatchSize):
    print("Connecting to Supabase...")
    try:
        supabase: Client = create_client(sec.SUPABASE_URL, sec.SUPABASE_KEY)
        print("Connected")
        response = supabase.table(idsTable).select("l_id").eq("processed", False).limit(IDBatchSize).execute()
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
            response = (supabase.table(idsTable).update({"processed": True}).eq("l_id", row["l_id"]).execute())
    except Exception as e:
        print("Supabase update failure: ", e)

def updateJobStatus(id, status, checked):
    print("Connecting to Supabase...")
    try:
        supabase: Client = create_client(sec.SUPABASE_URL, sec.SUPABASE_KEY)
        print("Connected")
        
        existing_data = supabase.table(jobsTable).select(status).eq("l_id", id).execute()
        if existing_data.data and existing_data.data[0][status] == checked:
            print(f"Skipping update: Job {id} {status} is already {checked}")
            return
        
        print(f"Updating job {id} {status} to {checked}")
        response = (supabase.table(jobsTable).update({status: checked}).eq("l_id", id).execute())
    except Exception as e:
        print("Supabase status update failure: ", e)

from supabase import create_client, Client
import os
import app_secrets as sec  # Ensure you have your Supabase credentials stored securely

# Initialize Supabase Client
supabase: Client = create_client(sec.SUPABASE_URL, sec.SUPABASE_KEY)

def selectFromTable(filters=None):
    try:
        print("Connecting to Supabase...")
        supabase: Client = create_client(sec.SUPABASE_URL, sec.SUPABASE_KEY)
        print("Connected")
        print(f"Select on: {filter}")
        query = supabase.table(jobsTable).select("*")

        # Apply filters dynamically
        if filters:
            for column, value in filters.items():
                query = query.eq(column, value)

        response = query.execute()
        return response.data  # Returns list of records

    except Exception as e:
        print("Supabase selection error:", e)
        return None


