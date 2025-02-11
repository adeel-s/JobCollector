import os
import google.generativeai as genai
import llm_prompts as prompts

apiKey = os.environ.get("GEMINI_API_KEY")


description = ""
prompt = prompts.jobDataExtractionPrompt
genai.configure(api_key=apiKey)
model = genai.GenerativeModel("gemini-1.5-flash")
response = ""

def extractData (description):
    response = model.generate_content(prompt + description).text.strip().strip("`")
    return response
    



