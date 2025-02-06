from datetime import datetime
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from documents import resume_template as resTemplate
from documents import cover_letter_template as clTemplate
from documents import description as desc
import services.resume_generation_service as resGen
import services.cover_letter_generation_service as letterGen
import services.file_conversion_service as convert

# Generate bullets
# description = desc.description



def generate(description):
    resume = resTemplate.resume
    coverLetter = clTemplate.template
    resumeFilePath = "documents\\resume.md"
    resumePDFPath = "documents\\resume.pdf"
    coverLetterFilePath = "documents\\cover_letter.md"
    coverLetterPDFPath = "documents\\cover_letter.pdf"
    # TODO: MOVE BULLET INSERTION INTO THE COVERLETTERGENERATOR FILE
    print("Inserting bullet points into resume...")
    try:
        bullets = resGen.generate(description)
        # Fill placeholders with bullets
        i = 0
        while "!@#$Placeholder" in resume and i < len(bullets):
            #print(bullets[i])
            resume = resume.replace("!@#$Placeholder", bullets[i], 1)
            i += 1

        print("Done with bullet point insertion")

        print("Writing to output file...")

        # Write resume to output file
        with open(resumeFilePath, "w", encoding="utf-8") as file:
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

        with open(coverLetterFilePath, "w", encoding="utf-8") as file:
            file.write(coverLetter)
        convert.MDtoPDF(coverLetterFilePath, coverLetterPDFPath)
        convert.MDtoPDF(resumeFilePath, resumePDFPath)

    except Exception as e:
        print(f"Failed with exception: {e}")
        raise Exception("Material Generation Failed")
    

