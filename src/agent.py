import requests
import json
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import time #import time

app = Flask(__name__)
CORS(app)

HUGGINGFACE_API_TOKEN = os.getenv("HUGGINGFACE_API_TOKEN")
HUGGINGFACE_API_URL = "https://api-inference.huggingface.co/models/google/gemma-2b-it"

headers = {"Authorization": f"Bearer {HUGGINGFACE_API_TOKEN}"}

conversation_history = []

def query(payload):
    try:
        print(f"Sending payload: {json.dumps(payload)}")
        response = requests.post(HUGGINGFACE_API_URL, headers=headers, json=payload)
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

def generate_response(user_input):
    global conversation_history
    history_text = "\n".join(conversation_history)
    prompt = f"""
    You are a helpful and encouraging conversational AI agent. Your goal is to encourage the user to develop their english speaking and communication skills. 
    You are proficient in having conversation with the user on diverse topics focussing on developing the user's skills along 
    the following themes: Communication, Ethics, Gender Sensitivity, Critical Thinking and Entrepreneurship. 
    You have to keep in mind not to make any personal remarks or make any comments on the user based on their replies.
    Try to ask open ended questions, and encourage the user to speak more. Keep your responses short and to the point. 
    Only reply to User's last question. Avoid using any special characters or symbols in your response. Stick to plain text.
    Do not provide any information that is not directly related to the user's input.

    {history_text}

    User: {user_input}
    AI: 
    """
    output = query({
        "inputs": prompt,
    })
    if isinstance(output, list) and output:
        full_response = output[0]['generated_text']
        parts = full_response.split("AI: ")
        if isinstance(parts, list) and len(parts) > 1:
            ai_response = parts[-1].strip()
        else:
            ai_response = full_response.strip()
        conversation_history.append(f"User: {user_input}")
        conversation_history.append(f"AI: {ai_response}")
        if len(conversation_history) > 10:
            conversation_history = conversation_history[-10:]
        return ai_response
    else:
        return "Error: Could not generate response."

@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.get_json()
    user_input = data.get('message')
    if user_input:
        ai_response = generate_response(user_input)
        time.sleep(1) #add a 1 second delay.
        return jsonify({'ai_response': ai_response})
    else:
        return jsonify({'error': 'No message provided'}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)