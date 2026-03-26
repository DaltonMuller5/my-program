import json
import os
import random
import hashlib
import datetime
from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from functools import wraps
from dotenv import load_dotenv

app = Flask(__name__)
app.secret_key = "datascience_secret_key_2024"

USERS_FILE = "users.json"
LOGINS_FILE = "login_log.json"

def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=2)

def load_login_log():
    if not os.path.exists(LOGINS_FILE):
        return []
    with open(LOGINS_FILE, "r") as f:
        return json.load(f)

def save_login_log(log):
    with open(LOGINS_FILE, "w") as f:
        json.dump(log, f, indent=2)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def log_login_attempt(username, success, ip):
    log = load_login_log()
    log.append({
        "username": username,
        "success": success,
        "ip": ip,
        "timestamp": datetime.datetime.now().isoformat(),
        "hour": datetime.datetime.now().hour
    })
    save_login_log(log)

def get_analytics():
    log = load_login_log()
    users = load_users()

    total_attempts = len(log)
    successful = sum(1 for e in log if e["success"])
    failed = total_attempts - successful
    success_rate = round((successful / total_attempts * 100), 1) if total_attempts > 0 else 0

    # Logins per hour (last 24h simulation)
    hour_counts = [0] * 24
    for entry in log:
        h = entry.get("hour", 0)
        if entry["success"]:
            hour_counts[h] += 1

    # Simulate extra data if sparse
    if sum(hour_counts) < 10:
        simulated = [random.randint(1, 8) for _ in range(24)]
        # peak hours
        for h in [8, 9, 10, 14, 15, 16, 20, 21]:
            simulated[h] += random.randint(3, 10)
        hour_counts = simulated

    # Recent attempts
    recent = log[-5:][::-1] if log else []

    # User count
    user_count = len(users)

    # Failed login usernames (top)
    failed_users = {}
    for e in log:
        if not e["success"]:
            failed_users[e["username"]] = failed_users.get(e["username"], 0) + 1
    top_failed = sorted(failed_users.items(), key=lambda x: x[1], reverse=True)[:3]

    return {
        "total_attempts": total_attempts,
        "successful": successful,
        "failed": failed,
        "success_rate": success_rate,
        "hour_counts": hour_counts,
        "recent": recent,
        "user_count": user_count,
        "top_failed": top_failed
    }

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    message = ""
    msg_type = ""
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        users = load_users()
        if not username or not password:
            message = "Please fill in all fields."
            msg_type = "error"
        elif len(password) < 4:
            message = "Password must be at least 4 characters."
            msg_type = "error"
        elif username in users:
            message = f"Username '{username}' is already taken."
            msg_type = "error"
        else:
            users[username] = {
                "password": hash_password(password),
                "created_at": datetime.datetime.now().isoformat()
            }
            save_users(users)
            message = f"Account created successfully! Welcome, {username}."
            msg_type = "success"
    return render_template("register.html", message=message, msg_type=msg_type)

@app.route("/login", methods=["GET", "POST"])
def login():
    message = ""
    msg_type = ""
    analytics = get_analytics()
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        users = load_users()
        ip = request.remote_addr
        if username in users and users[username]["password"] == hash_password(password):
            log_login_attempt(username, True, ip)
            session["user"] = username
            message = f"Welcome back, {username}! Login successful."
            msg_type = "success"
            analytics = get_analytics()
        else:
            log_login_attempt(username, False, ip)
            message = "Invalid username or password."
            msg_type = "error"
            analytics = get_analytics()
    return render_template("login.html", message=message, msg_type=msg_type, analytics=analytics)

@app.route("/api/analytics")
def api_analytics():
    return jsonify(get_analytics())

if __name__ == "__main__":
    app.run(debug=True, port=5000)