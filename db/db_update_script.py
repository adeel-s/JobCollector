import sqlite3, supabase, pandas as pd
import db_service as db
from datetime import datetime

# Select all from Supbase/Sqlite table jobs 
# yoe = yoe[0]
# Write all to jobs_backup
# Check jobs_backup and job_ids_backup
# Reinitialize jobs, refert selectAllJobs query to jobs instead of jobs_backup
# Pull in new data to validate yoe = int constraint is working
# Transfer back table data to main tables

jobs = pd.DataFrame(db.selectFromJobs())

# for index, row in jobs.iterrows():
#     print(row["company"], row["yoe"])
for index, row in jobs.iterrows():
    jobs.at[index, "yoe"] = int(row["yoe"][0])
    
jobs["posted"] = jobs["posted"].apply(lambda x: x.strftime("%Y-%m-%d %H:%M:%S") if isinstance(x, pd.Timestamp) and not pd.isna(x) else x)
jobs["created"] = jobs["created"].apply(lambda x: x.strftime("%Y-%m-%d %H:%M:%S") if isinstance(x, pd.Timestamp) and not pd.isna(x) else x)

print("------------------------DONE PROCESSING---------------------------")

# for index, row in jobs.iterrows():
#     print(row["company"], row["yoe"])

db.writeDFSupabase(jobs, "jobs")

db.writeDFSqlite(jobs, "jobs")




#jobIDs = pd.DataFrame(db.getAllIDs)
#db.writeDFSupabase(jobIDs, "job_ids_backup")
#db.writeDFSqlite(jobIDs, "job_ids_backup")