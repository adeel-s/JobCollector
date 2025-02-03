import sqlite3, pandas as pd, os, sys, json, psycopg2
from supabase import create_client, Client
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from psycopg2 import pool, extras
from psycopg2.sql import SQL, Identifier
import app_secrets as sec

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
        supabase.table(table).upsert(data, on_conflict=["l_id"], ignore_duplicates=True).execute()
        return True
    except Exception as e:
        print("Supabase access failure: ", e)
        return False
    

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
    jobsDF = pd.DataFrame(selectFromJobs())
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
        return True
    except Exception as e:
        print("Supabase update failure: ", e)
        return False

def resetJobIDs():
    print("Connecting to Supabase...")
    try:
        supabase: Client = create_client(sec.SUPABASE_URL, sec.SUPABASE_KEY)
        print("Connected")
        
        print("Marking job ids as processed")
        ids = getAllIDs()
        for i in ids:
            response = (supabase.table(idsTable).update({"processed": False}).eq("l_id", i["l_id"]).execute())
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
    
def selectFromJobs(jobFilter=None):
    try:
        print("Connecting to Supabase...")
        connection_pool = pool.SimpleConnectionPool(
            maxconn=10,
            minconn=1,
            user="postgres.wcqruutxfjomblzltiyo",
            password=sec.SUPABASE_PASSWORD,
            host="aws-0-us-east-2.pooler.supabase.com",
            port=6543,
            dbname="postgres",
        )

        conn = connection_pool.getconn()  # Get a connection from the pool
        cursor = conn.cursor(cursor_factory=extras.DictCursor)
        
        print(f"Select on: {jobFilter}")
        query, values = generateQuery(jobFilter)
        print(query, values)
        cursor.execute(query, values)
        rows = cursor.fetchall()
        #print(rows)
        jobs = [dict(row) for row in rows]

        connection_pool.putconn(conn)  # Return connection to the pool        print("Connected")
        return jobs  # Returns list of records

    except Exception as e:
        print("Supabase selection error:", e)
        return None
    

def generateQuery(filters):
    """
    Generates a dynamic SQL query based on the given filters.
    :param filters: Dictionary of filter conditions
    :return: SQL query string and parameter values
    """
    baseQuery = SQL("SELECT * FROM jobs WHERE 1=1")
    if not filters:
        return baseQuery, ()
    try:
        conditions = []
        values = []
        statuses = {"applied": False, "rejected": False, "saved": False, "not_interested": False}
        status_conditions = []
        if "status" in filters:
            for status in filters["status"]:
                statuses[status] = True
        for status, value in statuses.items():
            status_conditions.append(SQL("{} = %s").format(Identifier(status)))
            values.append(value)

        if status_conditions:
            conditions.append(SQL(" AND ").join(status_conditions))

        if "pay" in filters:
            conditions.append(SQL("{} != %s").format(Identifier("pay")))
            values.append("Pay not stated")

        location_conditions = []
        if "location" in filters and filters["location"]:
            
            for location in filters["location"]:
                location_conditions.append(SQL("{} ILIKE %s").format(Identifier("location")))
                values.append(f"%{location}%")  # Using f-string for clarity
    
        # Combine all conditions using OR
        if location_conditions:
            conditions.append(SQL(" OR ").join(location_conditions))

        # Handle location, arrangement, and pay filters (IN clauses)
        for key in ["arrangement"]:
            if key in filters and filters[key]:
                conditions.append(SQL("{} IN %s").format(Identifier(key)))
                values.append(tuple(filters[key]))

        if "yoe" in filters:
            yoe = filters["yoe"][-1] # Take the highest yoe value
            conditions.append(SQL("{} <= %s").format(Identifier("yoe")))
            values.append(yoe)


        # Handle "posted" filter (Sorting by most recent)
        order_by = SQL("")
        if "posted" in filters and "Most recent" in filters["posted"]:
            order_by = SQL("ORDER BY posted DESC NULLS LAST")

        # Combine all conditions into the query
        if conditions:
            baseQuery = baseQuery + SQL(" AND ") + SQL(" AND ").join(conditions)

        # Final query with sorting
        final_query = baseQuery + order_by
        return final_query, values
    except Exception as e:
        print(f"Query generation failed with exception: {e}")
    return

def dbReporting():
    jobsDF = pd.DataFrame(selectFromJobs())
    idsDF = pd.DataFrame(getAllIDs())
    numJobRecords = len(jobsDF)
    numIDRecords = len(idsDF)
    numProcessedJobsReported = 0

    for index, row in idsDF.iterrows():
        if row["processed"]:
            numProcessedJobsReported += 1

    print(f"""
        ---------------------------------------------
          
                     DATABASE REPORTING 
                     
        > Number of jobs in jobs table:        {numJobRecords}
        > Number of IDs in ids table:          {numIDRecords}
        > Number of IDs reported as processed: {numProcessedJobsReported}
        
                        END OF REPORT
        ---------------------------------------------
        """)