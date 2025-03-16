from agent import query, conversation_history
import json

def generate_response(user_input):
    global conversation_history
    model_name = "llama3.2:1b"
    model_config = {
        "api_url": "http://localhost:11434/api/chat",
        "response_key": "message",
        "answer_key": "content: "
    }
    conversation_history.append({"role": "user", "content": user_input})
    print(f"Conversation history: {json.dumps(conversation_history)}")
    output = query(model_name, {
        "model": model_name,
        "messages": conversation_history,
        "stream": False
    })
    print(f"API output: {json.dumps(output)}")
    
    if isinstance(output, dict) and model_config["response_key"] in output:
        message_content = output[model_config["response_key"]]["content"]
        if len(message_content) > 0:
            ai_response = message_content
        else:
            ai_response = f"Error: Could not find the response."
        conversation_history.append({"role": "assistant", "content": ai_response})
        if len(conversation_history) > 10:
            conversation_history = conversation_history[-10:]
        return ai_response
    else:
        return "Error: Could not generate response."