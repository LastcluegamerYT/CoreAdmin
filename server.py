from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
from gtts import gTTS
import os
import uuid

app = Flask(__name__)
CORS(app)  # This enables CORS for all domains

# Ensure the audio directory exists at startup
AUDIO_DIR = os.path.join(os.getcwd(), "audios")
os.makedirs(AUDIO_DIR, exist_ok=True)

@app.route("/generate-tts", methods=["POST"])
def generate_tts():
    try:
        data = request.json
        text = data.get("text", "").strip()

        if not text:
            return jsonify({"error": "Text is required"}), 400

        # Generate unique filename
        filename = f"{uuid.uuid4()}.mp3"
        filepath = os.path.join(AUDIO_DIR, filename)

        # Generate audio using gTTS
        print(f"🔊 Generating TTS for: {text[:50]}...")  # Truncated preview
        tts = gTTS(text=text, lang="hi", slow=False)
        tts.save(filepath)

        print(f"✅ Audio saved at: {filepath}")
        return jsonify({"audio_url": f"/audios/{filename}"}), 200

    except Exception as e:
        print("❌ TTS Generation Error:", str(e))
        return jsonify({"error": str(e)}), 500

@app.route("/audios/<filename>")
def serve_audio(filename):
    filepath = os.path.join(AUDIO_DIR, filename)

    if os.path.exists(filepath):
        print(f"🎧 Serving audio file: {filename}")
        return send_file(filepath, mimetype="audio/mpeg")
    else:
        print(f"⚠️ File not found: {filename}")
        return jsonify({"error": "File not found"}), 404

@app.route("/", methods=["GET"])
def index():
    return "✅ TTS Server is Running!", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
