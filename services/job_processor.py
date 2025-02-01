from datetime import datetime
import json
import random
import time
from bs4 import BeautifulSoup
import requests
import services.timestamp_service as ts
import pandas as pd
import services.data_extraction_service as ds
from db import db_service as db


delayWidth = 90
debuggingCSV = "debugging_csv\\new_processed_jobs.csv"
debuggingCSV1 = "debugging_csv\\new_scraped_jobs.csv"
jobsTableName = "jobs"
geminiDelay = 61

def getJobDetails(idBatch, LIRequestLimit, LIRequestDelay):
    jobs = []
    target_url='https://www.linkedin.com/jobs-guest/jobs/api/jobPosting/{}'
    for i in range(len(idBatch)):
        # Delay on reaching the request limit
        # TODO: Fix request limit after debugging implementation
        if i % LIRequestLimit == LIRequestLimit - 1:
            #nap = random.randint(LIRequestDelay - int(delayWidth/2), LIRequestDelay + int(delayWidth/2))
            nap = random.randint(15, 45)
            print("Sleeping for %s seconds" %nap)
            time.sleep(nap)
        resp = requests.get(target_url.format(idBatch[i]))
        soup=BeautifulSoup(resp.text,'html.parser')
        # Get company name
        job={}
        job["l_id"]=idBatch[i]
        try:
            job["company"]=soup.find("div",{"class":"top-card-layout__card"}).find("a").find("img").get('alt')
        except:
            job["company"]=None
        # Get position title
        try:
            job["title"]=soup.find("div",{"class":"top-card-layout__entity-info"}).find("a").text.strip()
        except:
            job["title"]="No job title provided - "

        try:
            job["location"]=soup.find("span",{"class":"topcard__flavor topcard__flavor--bullet"}).text.strip()
        except:
            job["location"]=None
        # Get seniority level
        try:
            job["level"]=soup.find("ul",{"class":"description__job-criteria-list"}).find("li").text.replace("Seniority level","").strip()
        except:
            job["level"]=None
        # posted-time-ago__text posted-time-ago__text--new topcard__flavor--metadata
        try:
            postedText = soup.find("span",{"class":"posted-time-ago__text posted-time-ago__text--new topcard__flavor--metadata"}).text.strip()
            job["posted"]=ts.getTimestamp(postedText)
        except:
            job["posted"]=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            job["url"]=soup.find("a",{"class":"topcard__link"}).get("href")
        except:
            job["url"]=None
        try:
            description = soup.find("div",{"class":"show-more-less-html__markup"}).contents
            job["description"]=str(description)
        except:
            job["description"]="No job description provided - "
        jobs.append(job)
        
    print("Finished collecting job details")
    #TODO: Make sure no data loss or bad format here
    jobs = pd.DataFrame(jobs)
    jobs.to_csv(debuggingCSV1, index=False, encoding='utf-8')
    return jobs

def processJobDescriptions(jobs, gemeniRequestLimit):
    newColumns = []
    for i, row in jobs.iterrows():
        if i % gemeniRequestLimit == gemeniRequestLimit - 1:
            print("Sleeping for %s seconds" %geminiDelay)
            time.sleep(geminiDelay)
        extractDataInput = row["title"] + " " + row["description"]
        extractedData = ds.extractData(extractDataInput)
        if extractedData:
            extractedData = json.loads(extractedData)
            newColumns.append(extractedData)
    newDf = pd.DataFrame(newColumns)

    for col in newDf.columns:
        jobs[col] = newDf[col]

    # Mediate experience level and YoE

    for index, row in jobs.iterrows():
        # Merge experience
        if row["level"] == "Not Applicable":
            jobs.at[index, "level"] = row["experience"]
        # Consolidate into YoE
        if not row["yoe"]:
            if row["level"] == "Entry Level":
                jobs.at[index, "yoe"] = "0"
            elif row["level"] == "Junior":
                jobs.at[index, "yoe"] = "2"
            else:
                jobs.at[index, "yoe"] = "3"
        else:
            jobs.at[index, "yoe"] = row["yoe"][0]

    jobs = jobs.drop(columns="experience")
    for column in jobs.columns:
        for index, value in enumerate(jobs[column]):
            try:
                json.dumps(value)  # Attempt to serialize
            except TypeError:
                print(f"Non-serializable value found in column '{column}' at index {index}: {value} ({type(value)})")
    db.writeDFSupabase(jobs, jobsTableName)
    db.updateJobIDs(jobs)
    jobs.to_csv(debuggingCSV, index=False, encoding='utf-8')
    return jobs

def processJobs(idBatch, LIRequestLimit, LIRequestDelay, gemeniRequestLimit):
    jobs = getJobDetails(idBatch, LIRequestLimit, LIRequestDelay)
    jobs = processJobDescriptions(jobs, gemeniRequestLimit)
    


    #TODO: STILL NEED TO RATE LIMIT GEMINI REQUESTS
