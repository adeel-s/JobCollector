from flask import Flask, render_template
import sqlite3
from db import db_service as db

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('db\\database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    jobs = db.getJobs()
    conn.close()
    return render_template("index.html", jobs=jobs)

