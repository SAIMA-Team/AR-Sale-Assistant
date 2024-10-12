from flask import Flask, request, jsonify, send_file
import requests
import io

app = Flask(__name__)

AUDIO_TO_TEXT_URL = "http://127.0.0.1:5001/convert"
TEXT_TO_AUDIO_URL = "http://127.0.0.1:5002/speak"
GENERATE_RESPONSE_URL = " http://127.0.0.1:5003/generate"
SELECT_ANIMATION_URL = "http://127.0.0.1:5004/select"

# This will hold the last generated audio content in memory for the demo
audio_data = None

@app.route('/process', methods=['POST'])
def process_request():
    global audio_data  # Reference to hold audio data in memory
    
    if 'audio' not in request.files:
        return jsonify({"error": "No audio file provided"}), 400

    audio_file = request.files['audio']

    # Step 1: Convert audio to text
    files = {'audio': (audio_file.filename, audio_file.read())}
    audio_to_text_response = requests.post(AUDIO_TO_TEXT_URL, files=files)
    if audio_to_text_response.status_code != 200:
        return jsonify(audio_to_text_response.json()), audio_to_text_response.status_code

    user_input = audio_to_text_response.json()['text']

    # Step 2: Generate response
    generate_response_payload = {'user_input': user_input}
    generate_response_result = requests.post(GENERATE_RESPONSE_URL, json=generate_response_payload)
    if generate_response_result.status_code != 200:
        return jsonify(generate_response_result.json()), generate_response_result.status_code

    response_text = generate_response_result.json()['response']

    # Step 3: Convert text to speech (MP3)
    text_to_audio_payload = {'text': response_text}
    text_to_audio_response = requests.post(TEXT_TO_AUDIO_URL, json=text_to_audio_payload)
    if text_to_audio_response.status_code != 200:
        return jsonify({"error": "Failed to convert text to speech"}), 500

    # Save the audio data for retrieval in the `get_audio` route
    audio_data = io.BytesIO(text_to_audio_response.content)
    audio_data.seek(0)

    # Step 4: Select animation
    select_animation_payload = {'response': response_text}
    select_animation_result = requests.post(SELECT_ANIMATION_URL, json=select_animation_payload)
    if select_animation_result.status_code != 200:
        return jsonify(select_animation_result.json()), select_animation_result.status_code

    animation = select_animation_result.json()['animation']

    # Prepare the final response
    return jsonify({
        "user_input": user_input,
        "response_text": response_text,
        "animation": animation
    }), 200, {
        'Content-Type': 'application/json',
        'X-Audio-Url': request.host_url + 'audio'  # URL to fetch the audio separately
    }

@app.route('/audio', methods=['GET'])
def get_audio():
    # Serve the last generated audio file as MP3
    if audio_data:
        return send_file(audio_data, mimetype="audio/mp3", as_attachment=True, download_name="response.mp3")
    return jsonify({"error": "No audio available"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
