from flask import Flask, jsonify, request
import json
import os

app = Flask(__name__)
DATA_FILE = "data.json"

def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

@app.route("/jobs", methods=["GET"])
def get_jobs():
    return jsonify(load_data())

@app.route("/jobs/<int:job_id>", methods=["GET"])
def get_job(job_id):
    data = load_data()
    job = next((j for j in data if j["id"] == job_id), None)
    return jsonify(job) if job else ("Job not found", 404)

@app.route("/jobs", methods=["POST"])
def add_job():
    data = load_data()
    new_job = request.json
    new_job["id"] = max([j["id"] for j in data], default=0) + 1
    data.append(new_job)
    save_data(data)
    return jsonify(new_job), 201

@app.route("/jobs/<int:job_id>", methods=["PUT"])
def update_job(job_id):
    data = load_data()
    job = next((j for j in data if j["id"] == job_id), None)
    if not job:
        return ("Job not found", 404)
    for key, value in request.json.items():
        job[key] = value
    save_data(data)
    return jsonify(job)

@app.route("/jobs/<int:job_id>", methods=["DELETE"])
def delete_job(job_id):
    data = load_data()
    data = [j for j in data if j["id"] != job_id]
    save_data(data)
    return ("Deleted", 204)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
