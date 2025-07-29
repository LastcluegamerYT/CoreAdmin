from flask import Flask, request, send_file, jsonify
from gtts import gTTS
import os
import uuid

app = Flask(__name__)

@app.route("/generate-tts", methods=["POST"])
def generate_tts():
    try:
        data = request.json
        text = data.get("text", "")
        if not text:
            return jsonify({"error": "Text is required"}), 400

        filename = f"{uuid.uuid4()}.mp3"
        filepath = os.path.join("audios", filename)

        tts = gTTS(text=text, lang="hi", slow=False)
        tts.save(filepath)
        return jsonify({"audio_url": f"/audios/{filename}"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/audios/<filename>")
def serve_audio(filename):
    filepath = os.path.join("audios", filename)
    if os.path.exists(filepath):
        return send_file(filepath, mimetype="audio/mpeg")
    else:
        return "File not found", 404

if __name__ == "__main__":
    os.makedirs("audios", exist_ok=True)
    app.run(host="0.0.0.0", port=5000)
