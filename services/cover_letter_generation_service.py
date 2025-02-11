import google.generativeai as genai
import llm_prompts as prompts
from documents import experience as exp
import os

apiKey = os.environ.get("GEMINI_API_KEY")
experience = exp.experience


description = ""
promptStart = prompts.coverLetterGenerationPrompt
genai.configure(api_key=apiKey)
model = genai.GenerativeModel("gemini-1.5-flash")
response = ""

def generate (description):
    prompt = f"{promptStart} \n\n Here is my work experience: \n\n {experience} \n\n Here is the job description: \n\n {description}"
    response = model.generate_content(prompt).text.strip().strip("`")
    return response



    



