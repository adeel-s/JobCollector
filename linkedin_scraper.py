import csv
import requests
from bs4 import BeautifulSoup
import math
import pandas as pd

ids = []
output_file = "debugging_csv\\scraped_jobs.csv"
alljobs_on_this_page = []
magicNumber = 10
def scrape(numJobs):
    target_url='https://www.linkedin.com/jobs/search/?alertAction=viewjobs&currentJobId=4133952919&geoId=90000014&keywords=Software%20Engineer&origin=JOB_SEARCH_PAGE_SEARCH_BUTTON&refresh=true'
    k = []
    o = {}
    print("Opening search URL and collecting job IDs")
    for i in range(magicNumber): #change this later
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
    limitReqs = min(numJobs, len(ids))
    target_url='https://www.linkedin.com/jobs-guest/jobs/api/jobPosting/{}'
    for j in range(limitReqs):
        resp = requests.get(target_url.format(ids[j]))
        soup=BeautifulSoup(resp.text,'html.parser')
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

def outputData (jobList):
    print("Writing data to csv")
    df = pd.DataFrame(jobList)
    df.to_csv(output_file, index=False, encoding='utf-8')
            
    print("Finished writing data")
def runScrapingService(numJobs):
    outputData(scrape(numJobs))
