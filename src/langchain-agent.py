import requests
import json
from flask import Flask, request, jsonify
from flask_cors import CORS
# import os
import time
from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

app = Flask(__name__)
CORS(app)

OLLAMA_BASE_URL = "http://localhost:11434"

conversation_history = [
    SystemMessage( content="You are a supportive and motivational conversational AI designed to enhance the user's English speaking and communication skills. You are a personal mentor. You are not a virtual girlfriend, boyfriend, clinical therapist, or coach. Your primary focus is to foster conversations around the themes of Communication, Ethics, Gender Sensitivity, Critical Thinking, and Entrepreneurship. You will maintain an encouraging tone and avoid personal remarks or comments on the user's responses. Your responses should be concise and directly related to the user's last question (starting with 'User:'). Refrain from using special characters or symbols in your replies, and stick to plain text in all interactions. Always provide a direct and concise answer to the user's input. Do not include any internal reasoning or '<think>' sections in your replies. Focus solely on responding to the user's question or prompt.")
]

llm = ChatOllama(
    base_url=OLLAMA_BASE_URL,
    model="gemma3:1b",  # Specify the model name here
    temperature=0.8,  # Adjust the temperature for response variability
    # max_tokens=256,  # Set the maximum number of tokens for the response
    format="json"
)

 
@app.route('/send_message', methods=['POST'])
def send_message():
    global conversation_history  # Declare conversation_history as global

    data = request.get_json()
    print(f"Received data: {json.dumps(data)}")
    user_input = data.get('message')
    print(f"User Message: {user_input}")
    if not user_input:
        return jsonify({'error': 'No message provided'}), 400
    
    try:
        conversation_history.append(HumanMessage(content=user_input))
        print(f"Conversation history: {conversation_history}")
        # Check if the conversation history exceeds the limit
        if len(conversation_history) > 10:
            conversation_history = conversation_history[-10:]
        response = llm.invoke(conversation_history)
        print(f"API response: {response.content}")


        ai_response = response.content
        print(f"AI reponse: {ai_response}")
        
        conversation_history.append(AIMessage(content=ai_response))
        if len(conversation_history) > 10:
            conversation_history = conversation_history[-10:]
    
    except Exception as e:
        print(f"Error: An unexpected error occurred: {e}")
        return {"error": f"An unexpected error occurred: {e}"}
        
    return jsonify({'ai_response': ai_response})

if __name__ == '__main__':
    app.run(debug=True, port=5001)