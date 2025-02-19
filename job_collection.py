from services import job_id_collector as idc, job_processor as jp, smtp_service as txt

from db import db_service as db
searchURLs = ['https://www.linkedin.com/jobs/search/?currentJobId=4138895842&distance=25&f_E=1%2C2&f_TPR=r86400&geoId=90000014&keywords=Software%20Engineer&origin=JOB_SEARCH_PAGE_JOB_FILTER&refresh=true&sortBy=R',
              'https://www.linkedin.com/jobs/search/?currentJobId=4090955934&f_E=1%2C2&f_TPR=r86400&f_WT=2&geoId=103644278&keywords=software%20development%20engineer&origin=JOB_SEARCH_PAGE_SEARCH_BUTTON&refresh=true',
              'https://www.linkedin.com/jobs/search/?currentJobId=4144070505&f_E=1%2C2&f_TPR=r86400&geoId=111241134&keywords=software%20development%20engineer&origin=JOB_SEARCH_PAGE_JOB_FILTER&refresh=true',
              'https://www.linkedin.com/jobs/search/?currentJobId=3864452564&f_E=1%2C2&f_TPR=r86400&geoId=90000308&keywords=software%20development%20engineer&origin=JOB_SEARCH_PAGE_LOCATION_AUTOCOMPLETE&refresh=true',
              'https://www.linkedin.com/jobs/search/?currentJobId=4142547293&f_E=1%2C2&f_TPR=r86400&geoId=105240372&keywords=software%20development%20engineer&origin=JOB_SEARCH_PAGE_LOCATION_AUTOCOMPLETE&refresh=true']

#
# I DO want to parameterize request loading from this file
# Also, jobID collection and job processing should also be parallelized

# Run urls through job-ID collector
    # Requests rate-limited to 8 requests of 25 ids/request
    # Written to the database after every batch
    # One batch every 2-5 minutes 



def collect():
    LIRequestDelay = 60
    gemeniRequestLimit = 13
    LIRequestLimit = 15
    IDBatchSize = 27
    try:
        oldJobNum, oldIDNum = db.dbReporting()
        # Collect new job IDs from LinkedIn
        for url in searchURLs:
            idc.collectJobIDs(url, LIRequestLimit, LIRequestDelay)


        # Get a batch of unprocessed job IDs from the database
        idBatch = [list(d.values())[0] for d in db.getIDs(IDBatchSize)]
        #TODO: ENABLE WHILE LOOP
        while(idBatch):
            jp.processJobs(idBatch, LIRequestLimit, LIRequestDelay, gemeniRequestLimit)
            db.backupSupabase()
            print("Job batch complete")
            idBatch = [list(d.values())[0] for d in db.getIDs(IDBatchSize)]

        print("No jobs left to process")
        # idBatch = db.getIDs(IDBatchSize) # ENABLE WITH WHILE LOOP
        newJobNum, newIDNum = db.dbReporting()
        addedJobs = newJobNum - oldJobNum
        addedIDs = newIDNum - oldIDNum
        message = f"Job Collection Summary \nNew jobs added: {addedJobs} \nTotal jobs: {newJobNum} \nNew IDs added: {addedIDs} \nTotal IDs: {newIDNum}"

    except Exception as e:
        # Set up specific exception handling here
        # Ex. Gemini resources exceeded: exponential backoff
        # Modify delay/batch size/request limits
        # collect()
        message = f"Job collection failed with exception: {e}"
        print(message)
    txt.sendText(message)

collect()
