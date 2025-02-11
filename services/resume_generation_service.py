import os
import re
import google.generativeai as genai
import llm_prompts as prompts
from documents import experience as exp

apiKey = os.environ.get("GEMINI_API_KEY")
experience = exp.experience


description = ""
promptStart = prompts.resumeGenerationPrompt
genai.configure(api_key=apiKey)
model = genai.GenerativeModel("gemini-1.5-flash")
response = ""

def generate (description):
    prompt = f"{promptStart} \n\n Here is my work experience: \n\n {experience} \n\n Here is the job description: \n\n {description}"
    response = model.generate_content(prompt).text.strip()
    # print("Gemini response: ", response)
    return parse(response)

def parse (bulletsString):
    bulletsList = re.split(r'Experience \d+\n', bulletsString)[1:]  # Remove first empty split part
    bulletsList = [bp.strip() for bp in bulletsList]
    # print("BulletsList: ", bulletsList)
    return bulletsList
    



