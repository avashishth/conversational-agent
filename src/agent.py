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
        "content": "You are a supportive and motivational conversational AI designed to enhance the user's English speaking and communication skills. Your primary focus is to foster conversations around the themes of Communication, Ethics, Gender Sensitivity, Critical Thinking, and Entrepreneurship. You will maintain an encouraging tone and avoid personal remarks or comments on the user's responses. Your responses should be concise and directly related to the user's last question (starting with 'User:'). Refrain from using special characters or symbols in your replies, and stick to plain text in all interactions. Always provide a direct and concise answer to the user's input. Do not include any internal reasoning or '<think>' sections in your replies. Focus solely on responding to the user's question or prompt."
    }
]

def query(payload):
    try:
        print(f"Sending payload: {json.dumps(payload)}")
        response = requests.post(OLLAMA_API_URL, json=payload)
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
    conversation_history.append({"role": "user", "content": user_input})
    print(f"Conversation history: {json.dumps(conversation_history)}")
    output = query({
        "model": "deepseek-r1:1.5b",
        "messages": conversation_history,
        "stream": False
    })
    print(f"API output: {json.dumps(output)}")
    
    if isinstance(output, dict) and "message" in output:
        message_content = output["message"]["content"]
        answer_index = message_content.find("</think>")
        if answer_index != -1:
            ai_response = message_content[answer_index + len("Answer: "):].strip()
        else:
            ai_response = "Error: Could not find 'Answer:' in the response."
        conversation_history.append({"role": "assistant", "content": ai_response})
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
        time.sleep(1) # add a 1 second delay.
        return jsonify({'ai_response': ai_response})
    else:
        return jsonify({'error': 'No message provided'}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)