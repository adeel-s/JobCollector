from io import StringIO
import pandas as pd
import json
import services.data_extraction_service as ds
import services.linkedin_scraper as scraper
import sqlite3
from db import db_service as db

inputFile = "debugging_csv\\scraped_jobs.csv"
outputFile = "debugging_csv\\processed_jobs.csv"

#open csv file, read in all data
print("Scraping jobs")
scraper.runScrapingService(15)
print("Reading scraped jobs")
try:
    df = pd.read_csv(inputFile)
        # Convert the DataFrame to a list of lists
    data = df.values.tolist()
except:
    print(f"An error occurred while reading the input file")
print("All jobs have been read")
print("Extracting description information")
# process description of each job, append to data
# print(ds.extractData(data[0][6]))
# print(df)
newColumns = []
for index, row in df.iterrows():
    extractDataInput = row["title"] + " " + row["description"]
    extractedData = json.loads(ds.extractData(extractDataInput))
    newColumns.append(extractedData)
newDf = pd.DataFrame(newColumns)

for col in newDf.columns:
    df[col] = newDf[col]

# Mediate experience level and YoE

for index, row in df.iterrows():
    # Merge experience
    if row["level"] == "Not Applicable":
        df.at[index, "level"] = row["experience"]
    # Consolidate into YoE
    if not row["yoe"]:
        if row["level"] == "Entry Level":
            df.at[index, "yoe"] = "0-1"
        elif row["level"] == "Junior":
            df.at[index, "yoe"] = "2-4"
        else:
            df.at[index, "yoe"] = "4+"

df = df.drop(columns="experience")
    
# Write out into a new file
print("Writing to csv debugging file")
df.to_csv(outputFile, index=False, encoding='utf-8')
print("Done writing")

# Write to database
print("Connecting to the database")

db.writeDFSupabase(df, "jobs")
db.writeDFSqlite(df, "jobs")
# connection = sqlite3.connect('db\\database.db')
# print("Connected to the database")
# table_name = "jobs"
# try:
#     print("Writing to the database")
#     for _, row in df.iterrows():
#         connection.execute("""
#             INSERT OR IGNORE INTO jobs (l_id, company, title, location, level, url, description, yoe, arrangement)
#             VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
#         """, (row.l_id, row.company, row.title, row.location, row.level, row.url, row.description, row.yoe, row.arrangement))

#     connection.commit()

# except Exception as e:
#     print("Error while writing to database:", e)
# finally:
#     connection.close()
# print("Updated database, closed connection")


print("Done")
    

