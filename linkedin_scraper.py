import csv
import requests
from bs4 import BeautifulSoup
import math
import pandas as pd

target_url='https://www.linkedin.com/jobs/search/?alertAction=viewjobs&currentJobId=4133952919&geoId=90000014&keywords=Software%20Engineer&origin=JOB_SEARCH_PAGE_SEARCH_BUTTON&refresh=true'
ids = []
output_file = "scraped_jobs.csv"
alljobs_on_this_page = []
print("Opening search URL and collecting job IDs")
for i in range(6): #change this later
    res = requests.get(target_url.format(i))
    soup=BeautifulSoup(res.text,'html.parser')
    jobs=soup.find_all("li")
    
    for x in range(0,len(jobs)):
        jobID = jobs[x].find("div", {"class":"base-card"})
        if jobID:
            jobID = jobID.get('data-entity-urn').split(":")[3]
            ids.append(jobID)
        #print(jobID)
k = []
o = {}
target_url='https://www.linkedin.com/jobs-guest/jobs/api/jobPosting/{}'
limitReqs = min(5, len(ids))
for j in range(limitReqs):
    resp = requests.get(target_url.format(ids[j]))
    soup=BeautifulSoup(resp.text,'html.parser')
    # Get company name
    o["id"]=ids[j]
    try:
        o["company"]=soup.find("div",{"class":"top-card-layout__card"}).find("a").find("img").get('alt')
    except:
        o["company"]=None
    # Get position title
    try:
        o["job-title"]=soup.find("div",{"class":"top-card-layout__entity-info"}).find("a").text.strip()
    except:
        o["job-title"]=None

    try:
        o["job-location"]=soup.find("span",{"class":"topcard__flavor topcard__flavor--bullet"}).text.strip()
    except:
        o["job-title"]=None
    # Get seniority level
    try:
        o["level"]=soup.find("ul",{"class":"description__job-criteria-list"}).find("li").text.replace("Seniority level","").strip()
    except:
        o["level"]=None
    try:
        o["URL"]=soup.find("a",{"class":"topcard__link"}).get("href")
    except:
        o["description"]=None
    try:
        o["description"]=soup.find("div",{"class":"show-more-less-html__markup"}).contents
    except:
        o["description"]=None
    k.append(o)
    o={}

print("Finished collecting job IDs")

df = pd.DataFrame(k)
df.to_csv('scraped_jobs.csv', index=False, encoding='utf-8')
        
print("Done")