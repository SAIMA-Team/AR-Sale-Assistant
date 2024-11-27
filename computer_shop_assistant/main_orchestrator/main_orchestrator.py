from flask import Flask, request, jsonify, send_file
import requests
import io
import threading
import base64

app = Flask(__name__)

AUDIO_TO_TEXT_URL = "http://audio-to-text:5001/convert"
TEXT_TO_AUDIO_URL = "http://text-to-audio:5002/speak"
GENERATE_RESPONSE_URL = "http://generate-response:5003/generate"
SELECT_ANIMATION_URL = "http://select-animation:5004/select"

@app.route('/process', methods=['POST'])
def process_request():
    if 'audio' not in request.files:
        return jsonify({"error": "No audio file provided"}), 400

    audio_file = request.files['audio']

    # Step 1: Convert audio to text
    files = {'audio': (audio_file.filename, audio_file.read())}
    audio_to_text_response = requests.post(AUDIO_TO_TEXT_URL, files=files)
    if audio_to_text_response.status_code != 200:
        return jsonify(audio_to_text_response.json()), audio_to_text_response.status_code
    
    user_input = audio_to_text_response.json().get('text', '')

    # Step 2: Generate response
    generate_response_payload = {'user_input': user_input}
    generate_response_result = requests.post(GENERATE_RESPONSE_URL, json=generate_response_payload)
    if generate_response_result.status_code != 200:
        return jsonify(generate_response_result.json()), generate_response_result.status_code
    
    response_text = generate_response_result.json().get('response', '')

    # Step 3: Convert text to speech (WAV)
    text_to_audio_payload = {'text': response_text}
    text_to_audio_response = requests.post(TEXT_TO_AUDIO_URL, json=text_to_audio_payload)
    if text_to_audio_response.status_code != 200:
        return jsonify({"error": "Failed to convert text to speech"}), 500

    # Step 4: Select animation
    select_animation_payload = {'response': response_text}
    select_animation_result = requests.post(SELECT_ANIMATION_URL, json=select_animation_payload)
    if select_animation_result.status_code != 200:
        return jsonify(select_animation_result.json()), select_animation_result.status_code
    
    animation = select_animation_result.json().get('animation', '')

    # Prepare the response with audio data included
    response_data = {
        "user_input": user_input,
        "response_text": response_text,
        "animation": animation,
         "audio": base64.b64encode(text_to_audio_response.content).decode('utf-8')  # Encode to Base64  # Encode binary audio data as string
    }

    return jsonify(response_data), 200, {'Content-Type': 'application/json'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)