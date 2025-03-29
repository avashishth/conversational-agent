import requests
import json
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import time

app = Flask(__name__)
CORS(app)

OLLAMA_API_URL = "http://localhost:11434/api/chat"

conversation_history = [
    {
        "role": "system", 
        "content": "You are a supportive and motivational conversational AI designed to enhance the user's English speaking and communication skills. You are a personal mentor. You are not a virtual girlfriend, boyfriend, clinical therapist, or coach. Your primary focus is to foster conversations around the themes of Communication, Ethics, Gender Sensitivity, Critical Thinking, and Entrepreneurship. You will maintain an encouraging tone and avoid personal remarks or comments on the user's responses. Your responses should be concise and directly related to the user's last question (starting with 'User:'). Refrain from using special characters or symbols in your replies, and stick to plain text in all interactions. Always provide a direct and concise answer to the user's input. Do not include any internal reasoning or '<think>' sections in your replies. Focus solely on responding to the user's question or prompt."
    }
]

def query(model_name, payload):
    model_config = {
        "api_url": OLLAMA_API_URL
    }
    try:
        print(f"Sending payload: {json.dumps(payload)}")
        response = requests.post(model_config["api_url"], json=payload)
        response.raise_for_status()
        print(f"API response status code: {response.status_code}")
        try:
            response_json = response.json()
            print(f"API response JSON: {json.dumps(response_json)}")
            return response_json
        except requests.exceptions.JSONDecodeError:
            print("Error: Invalid JSON response from API.")
            print(f"Response text: {response.text}")
            return {"error": "Invalid JSON response from API"}
    except requests.exceptions.RequestException as e:
        print(f"Error: API request failed: {e}")
        return {"error": f"API request failed: {e}"}
    except Exception as e:
        print(f"Error: An unexpected error occurred: {e}")
        return {"error": f"An unexpected error occurred: {e}"}

@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.get_json()
    print(f"Received data: {json.dumps(data)}")
    user_input = data.get('message')
    model_name = data.get('model')
    
    if not user_input:
        return jsonify({'error': 'No message provided'}), 400
    
    if not model_name:
        return jsonify({'error': 'No model name provided'}), 400

    if model_name == 'deepseek-r1:1.5b':
        from models.deepseek_r1 import generate_response
    elif model_name == 'llama3-chatqa':
        from models.llama3_chatqa import generate_response
    else:
        return jsonify({'error': 'Invalid model name'}), 400

    ai_response = generate_response(user_input)
    time.sleep(1) # add a 1 second delay.
    return jsonify({'ai_response': ai_response})

if __name__ == '__main__':
    app.run(debug=True, port=5000)