import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from documents import resume_template as template
from documents import description as desc
import resume_experience_generation_service as expGen

# Generate bullets
description = desc.description
print("Sending experience and description to Gemini for generation...")
bullets = expGen.generate(description)
print("Done with bullet point generation")
resume = template.resume
filePath = "documents\\resume.md"


print("Inserting bullet points into resume...")

# Fill placeholders with bullets
i = 0
while "!@#$Placeholder" in resume and i < len(bullets):
    resume = resume.replace("!@#$Placeholder", bullets[i])
    i += 1

print("Done with bullet point insertion")

print("Writing to output file...")

# Write resume to output file
with open(filePath, "w") as file:
    file.write(resume)

print("Done writing to output file")


