import csv
import requests
from bs4 import BeautifulSoup
import math
import pandas as pd
import services.timestamp_service as ts

ids = []
output_file = "debugging_csv\\scraped_jobs.csv"
tempFile = "debugging_csv\\job_ids.csv"
alljobs_on_this_page = []

def outputData (jobList, file):
    print("Writing data to csv")
    df = pd.DataFrame(jobList)
    df.to_csv(file, index=False, encoding='utf-8')

def scrape(numJobs):
    target_url='https://www.linkedin.com/jobs/search/?currentJobId=4138259127&distance=25&f_TPR=r86400&geoId=90000014&keywords=Software%20Engineer&origin=JOB_SEARCH_PAGE_JOB_FILTER&refresh=true&sortBy=R'
    k = []
    o = {}

    print("Opening search URL and collecting job IDs")
    res = requests.get(target_url.format(0))
    soup=BeautifulSoup(res.text,'html.parser')
    totalJobs = soup.find("span", {"class":"results-context-header__job-count"}).text
    totalJobs = int(''.join(c for c in totalJobs if c.isdigit()))
    print(totalJobs)
    for i in range(5): #change this later
        res = requests.get(target_url.format(i))
        soup=BeautifulSoup(res.text,'html.parser')
        jobs=soup.find_all("li")
        for x in range(0,len(jobs)):
            jobID = jobs[x].find("div", {"class":"base-card"})
            if jobID:
                jobID = jobID.get('data-entity-urn').split(":")[3]
                ids.append(jobID)
            #print(jobID)
    print("Finished collecting job IDs, collected: %s" % str(len(ids)))
    outputData(ids, tempFile)
    limitReqs = min(numJobs, len(ids))
    target_url='https://www.linkedin.com/jobs-guest/jobs/api/jobPosting/{}'
    for j in range(limitReqs):
        resp = requests.get(target_url.format(ids[j]))
        soup=BeautifulSoup(resp.text,'html.parser')
        postingDate = " This job was posted "
        # Get company name
        o["l_id"]=ids[j]
        try:
            o["company"]=soup.find("div",{"class":"top-card-layout__card"}).find("a").find("img").get('alt')
        except:
            o["company"]=None
        # Get position title
        try:
            o["title"]=soup.find("div",{"class":"top-card-layout__entity-info"}).find("a").text.strip()
        except:
            o["title"]=None

        try:
            o["location"]=soup.find("span",{"class":"topcard__flavor topcard__flavor--bullet"}).text.strip()
        except:
            o["location"]=None
        # Get seniority level
        try:
            o["level"]=soup.find("ul",{"class":"description__job-criteria-list"}).find("li").text.replace("Seniority level","").strip()
        except:
            o["level"]=None
        # posted-time-ago__text posted-time-ago__text--new topcard__flavor--metadata
        try:
            postedText = soup.find("span",{"class":"posted-time-ago__text posted-time-ago__text--new topcard__flavor--metadata"}).text.strip()
            o["posted"]=ts.getTimestamp(postedText)
        except:
            o["posted"]=None
        try:
            o["url"]=soup.find("a",{"class":"topcard__link"}).get("href")
        except:
            o["url"]=None
        try:
            o["description"]=soup.find("div",{"class":"show-more-less-html__markup"}).contents
        except:
            o["description"]=None
        k.append(o)
        o={}
    print("Finished collecting job details")
    return k
            
    print("Finished writing data")
def runScrapingService(numJobs):
    outputData(scrape(numJobs), output_file)
