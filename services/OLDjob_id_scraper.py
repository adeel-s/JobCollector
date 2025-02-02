
import csv
import random
import time
import requests
from bs4 import BeautifulSoup
import math
import pandas as pd

ids = []
outputFile = "debugging_csv\\job_ids_alot_alot.csv"
alljobs_on_this_page = []
# headers = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
#     "Accept-Language": "en-US,en;q=0.9",
#     "Accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
#     "Accept-encoding" : "gzip, deflate, sdch, br",
#     "Referer": "https://www.linkedin.com/jobs/search/",
#     "DNT": "1",  # Do Not Track
#     "Connection": "keep-alive"
# }

# UAs = [
#     "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.3",
#     "Mozilla/5.0 (Macintosh; Intel Mac OS X x.y; rv:42.0) Gecko/20100101 Firefox/43.4",
#     "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36",
#     "Mozilla/5.0 (iPhone; CPU iPhone OS 11_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1",
#     "Mozilla/5.0 (iPad; U; CPU OS 3_2_1 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Mobile/7B405",
#     "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
#     "Mozilla/5.0 (Linux; Android 13; SM-A536B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36",
#     "Mozilla/5.0 (iPhone14,3; U; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Mobile/19A346 Safari/602.1",
#     "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
# ]

def outputCSV (jobList, file):
    print("Writing data to csv")
    df = pd.DataFrame(jobList)
    df.to_csv(file, index=False, header=False, encoding='utf-8', mode='a')

target_url='https://www.linkedin.com/jobs/search/?alertAction=viewjobs&currentJobId=4133952919&geoId=90000014&keywords=Software%20Engineer&origin=JOB_SEARCH_PAGE_SEARCH_BUTTON&refresh=true'
print("Opening search URL and collecting job IDs")
res = requests.get(target_url.format(0))
soup=BeautifulSoup(res.text,'html.parser')
totalJobs = soup.find("span", {"class":"results-context-header__job-count"}).text
totalJobs = int(''.join(c for c in totalJobs if c.isdigit()))
print(totalJobs)
# Hit each page in the infinite scroll: totalJobs/25
for i in range(math.ceil(totalJobs / 25)): # replace with totalJobs
    # Every 8th request, sleep for a random amount of time
    if i % 8 == 7:
        nap = random.randint(150, 300)
        print("Sleeping for %s seconds" %nap)
        time.sleep(nap)
    # Rotate user agents
    #headers["User-Agent"] = UAs[i%8]
    # Use a request header
    res = requests.get(target_url.format(i))
    print(res)
    soup=BeautifulSoup(res.text,'html.parser')
    jobs=soup.find_all("li")
    ids = []
    for x in range(0,len(jobs)):
        jobID = jobs[x].find("div", {"class":"base-card"})
        if jobID:
            jobID = jobID.get('data-entity-urn').split(":")[3]
            ids.append(jobID)
        #print(jobID)
    print("Writing id batch to csv")
    outputCSV(ids, outputFile)
print("Finished collecting job IDs, collected: %s" % str(len(ids)))
