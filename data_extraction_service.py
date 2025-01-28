import google.generativeai as genai
import app_secrets as sec

apiKey = sec.GEMINI_API_KEY


description = ""
prompt = '''
The following text is an html formatted job description for a software developer role. I need specific pieces of information from this text:

Years of experience (categorized as 0-1, 2-4, 4+)
Work arrangement (categorized as On-site, Hybrid, Remote - default is on-site)
Experience level (caterogized as Intern, Entry Level, Junior, Mid-level, senior)

Please output only the result in JSON format without any extra newline characters (for example: result = {yoe:"2-4", arrangement:"Remote", experience:"Junior"} without any leading or trailing comments

'''
genai.configure(api_key=apiKey)
model = genai.GenerativeModel("gemini-1.5-flash")
response = ""

def extractData (description):
    response = model.generate_content(prompt + description).text.strip().strip("`")
    return response
    



