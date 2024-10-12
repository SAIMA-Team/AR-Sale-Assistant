# select_animation_service.py

from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/select', methods=['POST'])
def select_animation():
    response = request.json.get('response')
    if not response:
        return jsonify({"error": "No response provided"}), 400

    response_lower = response.lower()
    
    if "good morning" in response_lower:
        animation = "wave_animation"
    elif "thank you" in response_lower:
        animation = "bow_animation"
    elif "goodbye" in response_lower:
        animation = "goodbye_wave_animation"
    elif "gpu" in response_lower:
        animation = "show_gpu_animation"
    elif "processor" in response_lower:
        animation = "show_processor_animation"
    else:
        animation = "neutral_animation"

    return jsonify({"animation": animation})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004)