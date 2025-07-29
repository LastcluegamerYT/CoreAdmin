from flask import Flask, request, jsonify, send_file
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # ✅ Enables CORS for all origins

@app.route("/generate-tts", methods=["POST"])
def generate_tts():
    text = request.json.get("text", "")
    
    # Fake logic: return a test audio file
    with open("test.wav", "rb") as f:
        return send_file(f, mimetype="audio/wav")

if __name__ == "__main__":
    app.run()
