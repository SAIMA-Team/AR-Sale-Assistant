from flask import Flask, request, send_file, jsonify
from gtts import gTTS
from pydub import AudioSegment   #import AudioSegment class form pydub libaray for handle audio format conversion
import io

app = Flask(__name__)

@app.route('/speak', methods=['POST'])
def text_to_speech():
    text = request.json.get('text')
    if not text:
        return jsonify({"error": "No text provided"}), 400

    try:
        # Create gTTS object and save to a BytesIO object as MP3
        tts = gTTS(text=text, lang='en')        #convert the text to audio suing gtts
        mp3_output = io.BytesIO()               #create a bytes stream in memory for store the audio data
        tts.write_to_fp(mp3_output)             #write the audio data to the stream
        mp3_output.seek(0)                      #resets to starting position of the stream

        # Convert MP3 BytesIO object to WAV using pydub
        audio_segment = AudioSegment.from_file(mp3_output, format="mp3")       # create an audio segment using the mp3_output
        wav_output = io.BytesIO()                                              # create a bytes stream in memory for store the audio data
        audio_segment.export(wav_output, format="wav")                         #store the audio in audio_segment object to bytes stream in wav format
        wav_output.seek(0)

        return send_file(wav_output, mimetype="audio/wav", as_attachment=True, download_name="speech.wav")
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
