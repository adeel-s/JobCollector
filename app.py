from flask import Flask, render_template, request, jsonify
import sqlite3
from db import db_service as db

app = Flask(__name__)

@app.route('/')
def index():
    filter = \
    {"applied": False, "rejected": False, "saved": False, "not_interested": False}
    jobs = db.selectFromTable(filter)
    return render_template("index.html", jobs=jobs)

@app.route("/update_status", methods=["POST"])
def update_status():
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

