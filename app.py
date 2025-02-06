from flask import Flask, render_template, request, jsonify
import sqlite3
from db import db_service as db
from services import material_generation_service as matGen

app = Flask(__name__)

@app.route('/')
def index():
    jobFilter = {"status":[], "posted": ["Most recent"]}
    jobs = db.selectFromJobs(jobFilter)
    return render_template("index.html", jobs=jobs, jobs_length=len(jobs))

@app.route("/generate_materials", methods=["POST"])
def generateMaterials():
    try:
        data = request.json
        jobDescription = data["jobDescription"]
        matGen.generate(jobDescription)
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
