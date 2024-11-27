from flask import Flask, request, send_file, jsonify
from gtts import gTTS
from pydub import AudioSegment
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

        # Convert MP3 BytesIO object to WAV using pydub
        audio_segment = AudioSegment.from_file(mp3_output, format="mp3")
        wav_output = io.BytesIO()
        audio_segment.export(wav_output, format="wav")
        wav_output.seek(0)

        return send_file(wav_output, mimetype="audio/wav", as_attachment=True, download_name="speech.wav")
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
