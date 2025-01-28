from io import StringIO
import pandas as pd
import json
import data_extraction_service as ds

inputFile = "scraped_jobs.csv"
outputFile = "processed_jobs.csv"

#open csv file, read in all data

data = []
print("Reading scrabed jobs")
try:
    df = pd.read_csv(inputFile)
        # Convert the DataFrame to a list of lists
    data = df.values.tolist()
except:
    print(f"An error occurred:")
print("All jobs have been read")
print("Extracting description information")
# process description of each job, append to data
# print(ds.extractData(data[0][6]))
# print(df)
newColumns = []
for desc in df["description"]:
    extractedData = json.loads(ds.extractData(desc))
    # print(extractedData)
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
    if not row["YoE"]:
        if row["level"] == "Entry Level":
            df.at[index, "YoE"] = "0-1"
        elif row["level"] == "Junior":
            df.at[index, "YoE"] = "2-4"
        else:
            df.at[index, "YoE"] = "4+"

df = df.drop(columns="experience")
    
# write out into a new file
df.to_csv(outputFile, index=False, encoding='utf-8')

print("Done")
    

