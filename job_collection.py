from services import job_id_collector as idc, job_processor as jp

from db import db_service as db
searchURLs = ['https://www.linkedin.com/jobs/search/?currentJobId=4138895842&distance=25&f_E=1%2C2&f_TPR=r86400&geoId=90000014&keywords=Software%20Engineer&origin=JOB_SEARCH_PAGE_JOB_FILTER&refresh=true&sortBy=R',
              'https://www.linkedin.com/jobs/search/?currentJobId=4137537653&f_E=1%2C2&f_TPR=r86400&f_WT=2&keywords=developer&origin=JOB_SEARCH_PAGE_LOCATION_SUGGESTION&refresh=true''https://www.linkedin.com/jobs/search/?currentJobId=4137537653&f_E=1%2C2&f_TPR=r86400&f_WT=2&keywords=developer&origin=JOB_SEARCH_PAGE_LOCATION_SUGGESTION&refresh=true']

#
# I DO want to parameterize request loading from this file
# Also, jobID collection and job processing should also be parallelized

# Run urls through job-ID collector
    # Requests rate-limited to 8 requests of 25 ids/request
    # Written to the database after every batch
    # One batch every 2-5 minutes 

LIRequestDelay = 120
gemeniRequestLimit = 14
LIRequestLimit = 15
IDBatchSize = 75

for url in searchURLs:
    idc.collectJobIDs(url, LIRequestLimit, LIRequestDelay)


# Get a batch of unprocessed job IDs from the database
idBatch = [list(d.values())[0] for d in db.getIDs(IDBatchSize)]
#TODO: ENABLE WHILE LOOP
# while(idBatch):
    # Send all unprocessed jobs to job collector
    # This method will also handle NLP data extraction
        # Eventually, paralellize this
    # Jobs are written to the database after every batch
jp.processJobs(idBatch, LIRequestLimit, LIRequestDelay, gemeniRequestLimit)
# idBatch = db.getIDs(IDBatchSize) # ENABLE WITH WHILE LOOP


# Back up Supabase tables
db.backupSupabase()
print("Job collection complete")