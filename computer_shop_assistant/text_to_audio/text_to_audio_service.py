from flask import Flask, request, send_file, jsonify
from gtts import gTTS
import io

app = Flask(__name__)

@app.route('/speak', methods=['POST'])
def text_to_speech():
    text = request.json.get('text')
    if not text:
        return jsonify({"error": "No text provided"}), 400

    try:
        # Create gTTS object and save to a BytesIO object as MP3
        tts = gTTS(text=text, lang='en')
        mp3_output = io.BytesIO()
        tts.write_to_fp(mp3_output)
        mp3_output.seek(0)

        return send_file(mp3_output, mimetype="audio/mp3", as_attachment=True, download_name="speech.mp3")
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)


