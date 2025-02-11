import os, logging
import sys
from flask import Flask, current_app, render_template, request, jsonify, send_file
import sqlite3
from db import db_service as db
from services import material_generation_service as matGen

app = Flask(__name__)

if __name__ == "__main__":
    logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
    ],
    )
    app.logger.setLevel(logging.INFO)
    app.run(host="0.0.0.0", port=8000)
    

@app.route('/')
def index():
    app.logger.info("Application home page loaded ######################################################################")
    jobFilter = {"status":[], "posted": ["Most recent"]}
    jobs = db.selectFromJobs(jobFilter)
    return render_template("index.html", jobs=jobs, jobs_length=len(jobs))

@app.route('/write')
def write():
    return render_template("write.html", jobs_length=0)

@app.route('/generate_cover_letter', methods=["POST"])
def generateCoverLetter():
    try:
        data = request.json
        jobDescription = data["jobDescription"]
        jobCompany = data["jobCompany"]
        coverLetterText = matGen.generate(jobDescription, jobCompany)[0]
        print(coverLetterText)
        return jsonify({"success": True, "coverLetterText": coverLetterText})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
    
@app.route('/export_cover_letter', methods=["POST"])
def exportCoverLetter():
    try:
        data = request.json
        coverLetterText = data["coverLetterText"]
        matGen.writeCoverLetter(coverLetterText)
        print(coverLetterText)
        return jsonify({"success": True})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
    
@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/download_resume')
def downloadResume():
    resumePath = os.path.join(app.root_path, 'documents', 'resume.pdf')
    return send_file(resumePath, as_attachment=True)

@app.route('/download_cover_letter')
def downloadCoverLetter():
    coverLetterPath = os.path.join(app.root_path, 'documents', 'cover_letter.pdf')
    return send_file(coverLetterPath, as_attachment=True)

@app.route("/generate_materials", methods=["POST"])
def generateMaterials():
    try:
        data = request.json
        jobDescription = data["jobDescription"]
        jobCompany = data["jobCompany"]
        matGen.generate(jobDescription, jobCompany)
        # TODO: Return materials somehow
        return jsonify({"success": True, "jobDescription": jobDescription})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/update_status", methods=["POST"])
def updateStatus():
    try:
        data = request.json
        job_id = data["job_id"]
        status = data["status"]
        checked = data["checked"]

        # Connect to DB
        db.updateJobStatus(job_id, status, checked)

        return jsonify({"success": True, "job_id": job_id, "status": status, "checked": checked})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
    
@app.route("/filter_jobs", methods=["POST"])
def filterJobs():
    try:
        data = request.json

        jobFilter = {}  # Use a different variable name since "filter" is a built-in function in Python

        try:
            for column, value in data.items():  # FIX: Use .items() to get key-value pairs
                if value:
                    jobFilter[column] = value  # Store the filter conditions
            print("Filter conditions:", jobFilter)  # Debugging
            jobs = db.selectFromJobs(jobFilter)
            return jsonify({"success": True, "jobs": jobs})
        except Exception as e:
            print("Error processing filters:", e)
        

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
