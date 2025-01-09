from flask import Flask, request, jsonify, render_template, send_from_directory
import os
import json
import datetime
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Base directory for data storage
BASE_DIR = "data"
USER_DATA_FILE = os.path.join(BASE_DIR, "user.json")
WORLD_CHAT_FILE = os.path.join(BASE_DIR, "world.json")

# Ensure base directory exists
os.makedirs(BASE_DIR, exist_ok=True)

# Helper functions
def load_json(file_path, default_data=None):
    if os.path.exists(file_path):
        try:
            with open(file_path, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            pass  # If JSON is invalid, return the default data
    return default_data if default_data else []

def save_json(file_path, data):
    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)

# Initialize files
if not os.path.exists(USER_DATA_FILE):
    save_json(USER_DATA_FILE, [])

if not os.path.exists(WORLD_CHAT_FILE):
    save_json(WORLD_CHAT_FILE, [])

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/submit_problem", methods=["POST"])
def submit_problem():
    data = request.json
    email = data.get("email")
    problem = data.get("problem")

    if not email or not problem:
        return jsonify({"status": "error", "message": "Email and problem are required"}), 400

    users = load_json(USER_DATA_FILE, [])
    users.append({"email": email, "problem": problem})
    save_json(USER_DATA_FILE, users)

    return jsonify({"status": "success", "message": "Problem submitted successfully"})

@app.route("/emails", methods=["GET"])
def get_emails():
    emails = load_json(USER_DATA_FILE, [])
    return jsonify({"emails": emails})  # Return data in a structured way


@app.route("/world_chat", methods=["GET", "POST"])
def world_chat():
    if request.method == "GET":
        chats = load_json(WORLD_CHAT_FILE, [])
        return jsonify({"chats": chats})
    elif request.method == "POST":
        data = request.json
        username = data.get("username")
        message = data.get("message")
        reply_to = data.get("reply_to", None)

        if not username or not message:
            return jsonify({"status": "error", "message": "Username and message are required"}), 400

        chats = load_json(WORLD_CHAT_FILE, [])
        chat_entry = {
            "username": username,
            "message": message,
            "timestamp": datetime.datetime.now().strftime("%I:%M %p"),
        }
        if reply_to:
            chat_entry["reply_to"] = reply_to
        chats.append(chat_entry)
        save_json(WORLD_CHAT_FILE, chats)

        return jsonify({"status": "success", "message": "Message sent"})

@app.route("/world_chat_page")
def world_chat_page():
    return render_template("world.html")

@app.route("/admin_panel")
def admin_panel():
    chats = load_json(WORLD_CHAT_FILE, [])
    users = load_json(USER_DATA_FILE, [])
    return render_template("admin.html", chats=chats, users=users)

@app.route("/clear_world_chat", methods=["POST"])
def clear_world_chat():
    save_json(WORLD_CHAT_FILE, [])
    return jsonify({"status": "success", "message": "World chat cleared"})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
