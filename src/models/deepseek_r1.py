from agent import query, conversation_history
import json

def generate_response(user_input):
    global conversation_history
    model_name = "deepseek-r1:1.5b"
    model_config = {
        "api_url": "http://localhost:11434/api/chat",
        "response_key": "message",
        "answer_key": "Answer: ",
        "strip_key": "</think>"
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
        answer_index = message_content.find(model_config["answer_key"])
        # Check for Answer: in the response
        if answer_index != -1:
            ai_response = message_content[answer_index:].strip()
        else:
            # If Answer: is not found, check for </think> in the response
            answer_index = message_content.find(model_config["strip_key"])
            if answer_index != -1:
                ai_response = message_content[answer_index:].strip()
            else:
                ai_response = f"Error: Could not find '{model_config['answer_key']}' in the response."
        conversation_history.append({"role": "assistant", "content": ai_response})
        if len(conversation_history) > 10:
            conversation_history = conversation_history[-10:]
        return ai_response
    else:
        return "Error: Could not generate response."