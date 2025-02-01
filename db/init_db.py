import sqlite3, pandas as pd
from supabase import create_client, Client
import sys, os
import db_service as db

# Get the parent directory and add it to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import app_secrets as sec
sqliteSchemaFile = 'db\\sqlite_schema.sql'
supabaseSchemaFile = 'db\\supabase_schema.sql'
localDatabase = 'db\\database.db'

jobsBackupTable = "jobs_backup"
jobIDsBackupTable = "job_ids_backup"
# Create a Supabase client

supabase: Client = create_client(sec.SUPABASE_URL, sec.SUPABASE_KEY)

connection = sqlite3.connect(localDatabase)

# Back up tables to Supabase backups

raise Exception("ENSURE BACKUP TABLES EXIST WITH NAMES: jobs_backup and job_ids_backup. ALSO CONSIDER EXPORTING CSV FILES")


jobs = pd.DataFrame(db.selectFromJobs())
jobs["posted"] = jobs["posted"].apply(lambda x: x.strftime("%Y-%m-%d %H:%M:%S") if isinstance(x, pd.Timestamp) and not pd.isna(x) else x)
jobs["created"] = jobs["created"].apply(lambda x: x.strftime("%Y-%m-%d %H:%M:%S") if isinstance(x, pd.Timestamp) and not pd.isna(x) else x)

ids = pd.DataFrame(db.getAllIDs())


db.writeDFSupabase(jobs, jobsBackupTable)

db.writeDFSupabase(ids, jobIDsBackupTable)

with open(sqliteSchemaFile) as f:
    try:
        #connection.executescript(f.read())
        connection.commit()
    except Exception as e:
        print(e)

with open(supabaseSchemaFile) as f:
    try:
        print()
        #response = supabase.rpc("pg_execute_sql", {"sql": f.read()}).execute()
        #print(response)
    except Exception as e:
        print(e)


    
connection.close()

