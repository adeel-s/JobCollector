from datetime import datetime
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from documents import resume_template as resTemplate
from documents import cover_letter_template as clTemplate
from documents import description as desc
import services.resume_generation_service as resGen
import services.cover_letter_generation_service as letterGen

# Generate bullets
description = desc.description
print("Sending experience and description to Gemini for generation...")
bullets = resGen.generate(description)
print("Done with bullet point generation")
resume = resTemplate.resume
coverLetter = clTemplate.template
resumeFilePath = "documents\\resume.md"
coverLetterFilePath = "documents\\cover_letter.md"

# TODO: MOVE BULLET INSERTION INTO THE COVERLETTERGENERATOR FILE
print("Inserting bullet points into resume...")

# Fill placeholders with bullets
i = 0
while "!@#$Placeholder" in resume and i < len(bullets):
    #print(bullets[i])
    resume = resume.replace("!@#$Placeholder", bullets[i], 1)
    i += 1

print("Done with bullet point insertion")

print("Writing to output file...")

# Write resume to output file
with open(resumeFilePath, "w") as file:
    file.write(resume)

print("Done writing to output file")


# TODO: MOVE THIS INTO THE COVERLETTERGENERATOR FILE
# Cover letter generation
letter = letterGen.generate(description)
date = datetime.now().strftime("%B %d, %Y").replace(" 0", " ")
placeholders = {"Date": date, "Company": "PLACEHOLDER COMPANY", "Letter": letter}

for attribute, value in placeholders.items():
    placeholder = f"!@#$Placeholder{attribute}"  # Construct the placeholder format
    coverLetter = coverLetter.replace(placeholder, str(value))

with open(coverLetterFilePath, "w") as file:
    file.write(coverLetter)

