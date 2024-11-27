from flask import Flask, request, jsonify
import speech_recognition as sr
from io import BytesIO
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)

# Limit the size of uploaded files (optional)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB limit

# Allowed audio file types
ALLOWED_EXTENSIONS = {'wav', 'mp3', 'flac'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/convert', methods=['POST'])
def convert_audio_to_text():
    if 'audio' not in request.files:
        return jsonify({"error": "No audio file provided"}), 400

    audio_file = request.files['audio']

    if audio_file.filename == '' or not allowed_file(audio_file.filename):
        return jsonify({"error": "Invalid audio file format"}), 400

    recognizer = sr.Recognizer()

    try:
        with sr.AudioFile(BytesIO(audio_file.read())) as source:
            audio_data = recognizer.record(source)
        text = recognizer.recognize_google(audio_data)
        return jsonify({"text": text})
    except sr.UnknownValueError:
        return jsonify({"error": "Could not understand audio"}), 400
    except sr.RequestError as e:
        logging.error(f"Request error: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
