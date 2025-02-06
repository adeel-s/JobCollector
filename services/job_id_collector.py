import random
import time
import requests
from bs4 import BeautifulSoup
import math
import pandas as pd
from db import db_service as db

ids = []
outputFile = "debugging_csv\\job_ids.csv"
pageSize = 25
tableName = "job_ids"
delayWidth = 90

def outputCSV (jobList, file):
    print("Writing data to csv")
    df = pd.DataFrame(jobList)
    df.to_csv(file, index=False, header=False, encoding='utf-8')

def collectJobIDs (url, LIRequestLimit, LIRequestDelay):
    res = requests.get(url.format(0))
    soup=BeautifulSoup(res.text,'html.parser')
    try:
        totalJobs = soup.find("span", {"class":"results-context-header__job-count"}).text
        totalJobs = int(''.join(c for c in totalJobs if c.isdigit()))
    except:
        print("Failed to locate job count on page. Taking the first 25")
        totalJobs = 25
    print(str(totalJobs) + " found at URL: " + url)

    for i in range(math.ceil(totalJobs / pageSize)): # replace with totalJobs
        if i % LIRequestLimit == 0 and i != 0:
            nap = random.randint(LIRequestDelay - int(delayWidth/2), LIRequestDelay + int(delayWidth/2))
            print("Sleeping for %s seconds" %nap)
            time.sleep(nap)

        res = requests.get(url.format(i))
        print(res)
        soup=BeautifulSoup(res.text,'html.parser')
        jobs=soup.find_all("li")
        ids = []

        for x in range(0,len(jobs)):
            jobID = jobs[x].find("div", {"class":"base-card"})
            if jobID:
                jobID = jobID.get('data-entity-urn').split(":")[3]
                ids.append(jobID)
        
        outputCSV(ids, outputFile)
        df = pd.DataFrame(ids, columns=["l_id"])
        db.writeDFSupabase(df, tableName)

    print("Finished ID batch of: %s jobs" % str(len(ids)))