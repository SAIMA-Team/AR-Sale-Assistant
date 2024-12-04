from flask import Flask, request, jsonify            #import Flask class from flask library.
import speech_recognition as sr                      #import speech recognition library
from io import BytesIO                               #import BytesIo class from io library store audio data in memory
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)

# Limit the size of uploaded files (optional)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB limit

# Allowed audio file types
ALLOWED_EXTENSIONS = {'wav', 'mp3', 'flac'}

def allowed_file(filename):           #return true when file extention is an allowed one
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/convert', methods=['POST'])
def convert_audio_to_text():
    if 'audio' not in request.files:                   #check file named audio in requested files
        return jsonify({"error": "No audio file provided"}), 400

    audio_file = request.files['audio']    #get the audio file

    if audio_file.filename == '' or not allowed_file(audio_file.filename):           #check weath audio file extention is empty or not allowed
        return jsonify({"error": "Invalid audio file format"}), 400

    recognizer = sr.Recognizer()            #initiate the recognizer object

    try:
        with sr.AudioFile(BytesIO(audio_file.read())) as source:        ##load the audio file to memory as a byte array stream and then use it as an audio source for recognizer
            audio_data = recognizer.record(source)                     #store the audio data in recognizer
        text = recognizer.recognize_google(audio_data)                 #convert the audio data to text using Google’s Speech-to-Text API
        return jsonify({"text": text})
    except sr.UnknownValueError:                                       #handle error related to recognizer can not handle the provided audio data
        return jsonify({"error": "Could not understand audio"}), 400
    except sr.RequestError as e:                                       #handle network and connection errors
        logging.error(f"Request error: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
