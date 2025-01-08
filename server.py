from flask import Flask, request, jsonify, render_template, send_from_directory
import os
import json
import datetime
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow CORS for frontend integration

# Base directory for user data
BASE_DIR = "user_data"

# Ensure base directory exists
os.makedirs(BASE_DIR, exist_ok=True)

@app.route('/')
def hello():
    return render_template('user.html')

# Helper functions
def get_user_dir(ip):
    user_dir = os.path.join(BASE_DIR, ip)
    os.makedirs(user_dir, exist_ok=True)
    return user_dir

def get_user_file_path(ip, filename):
    return os.path.join(get_user_dir(ip), filename)

def load_json(file_path, default_data=None):
    if os.path.exists(file_path):
        try:
            with open(file_path, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            pass  # If JSON is invalid, return the default data
    return default_data if default_data else {}

def save_json(file_path, data):
    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)

def delete_old_files():
    cutoff_date = datetime.datetime.now() - datetime.timedelta(days=5)
    for user_folder in os.listdir(BASE_DIR):
        user_dir = os.path.join(BASE_DIR, user_folder)
        messages_path = os.path.join(user_dir, "messages.json")

        if os.path.exists(messages_path):
            messages = load_json(messages_path, [])
            messages = [msg for msg in messages if datetime.datetime.fromisoformat(msg['timestamp']) > cutoff_date]
            save_json(messages_path, messages)

# Admin Endpoints
@app.route("/admin", methods=["GET"])
def admin_panel():
    if request.headers.get("Accept") == "application/json":
        # Return JSON data for fetch requests
        user_list = os.listdir(BASE_DIR)
        total_users = len(user_list)
        return jsonify({"user_list": user_list, "total_users": total_users})
    else:
        # Render HTML for direct browser visits
        user_list = os.listdir(BASE_DIR)
        total_users = len(user_list)
        return render_template("admin.html", user_list=user_list, total_users=total_users)


@app.route("/admin/user/<ip>", methods=["GET"])
def view_user_data(ip):
    user_dir = get_user_dir(ip)
    messages = load_json(get_user_file_path(ip, "messages.json"), [])
    notifications = load_json(get_user_file_path(ip, "notifications.json"), [])
    email = load_json(get_user_file_path(ip, "email.json"), {})
    files = []
    files_dir = os.path.join(user_dir, "files")
    if os.path.exists(files_dir):
        files = os.listdir(files_dir)
    return jsonify({"messages": messages, "notifications": notifications, "email": email, "files": files, "ip": ip})

@app.route("/admin/notify/<ip>", methods=["POST"])
def notify_user(ip):
    notification = request.json.get("message")
    notifications_path = get_user_file_path(ip, "notifications.json")
    notifications = load_json(notifications_path, [])
    notifications.append({"message": notification, "timestamp": datetime.datetime.now().isoformat()})
    save_json(notifications_path, notifications)
    return jsonify({"status": "success", "message": "Notification sent."})

@app.route("/admin/delete_old", methods=["POST"])
def delete_old():
    delete_old_files()
    return jsonify({"status": "success", "message": "Old messages deleted."})

# User Endpoints
@app.route("/user/send", methods=["POST"])
def user_send():
    ip = request.remote_addr

    # Process message
    content = request.form.get("content")
    email = request.form.get("email")
    file = request.files.get("file")
    file_path = None

    if file:
        user_dir = get_user_dir(ip)
        files_dir = os.path.join(user_dir, "files")
        os.makedirs(files_dir, exist_ok=True)
        file_path = os.path.join(files_dir, file.filename)
        file.save(file_path)

    # Save email for new users
    email_path = get_user_file_path(ip, "email.json")
    if not os.path.exists(email_path) and email:
        save_json(email_path, {"email": email})

    # Save message
    messages_path = get_user_file_path(ip, "messages.json")
    messages = load_json(messages_path, [])
    
    # Ensure `messages` is a list
    if not isinstance(messages, list):
        messages = []

    messages.append({
        "content": content,
        "file": file_path,
        "timestamp": datetime.datetime.now().isoformat()
    })
    save_json(messages_path, messages)

    return jsonify({"status": "success", "message": "Message sent."})


@app.route("/user/messages", methods=["GET"])
def user_messages():
    ip = request.remote_addr
    messages_path = get_user_file_path(ip, "messages.json")
    notifications_path = get_user_file_path(ip, "notifications.json")

    messages = load_json(messages_path, [])
    notifications = load_json(notifications_path, [])

    return jsonify({"messages": messages, "notifications": notifications})

@app.route("/user", methods=["GET"])
def user_panel():
    return render_template("user.html")

# Serve user-uploaded files
@app.route("/user/files/<ip>/<filename>", methods=["GET"])
def serve_user_file(ip, filename):
    files_dir = os.path.join(get_user_dir(ip), "files")
    return send_from_directory(files_dir, filename)

# Serve static files (CSS, JS, etc.)
@app.route('/static/<path:path>', methods=['GET'])
def static_files(path):
    return send_from_directory('static', path)

# Run server
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
