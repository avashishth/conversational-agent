# Conversational AI Agent (Flask Backend)

This Flask application provides a backend for a conversational AI agent, utilizing the Hugging Face Inference API for language model interactions. It maintains conversation history and provides a simple API for sending and receiving messages.

## Features

* **Hugging Face Inference API Integration:** Leverages powerful language models hosted on Hugging Face.
* **Conversation History:** Maintains context across multiple turns of a conversation.
* **Prompt Engineering:** Allows for customization of AI agent behavior through prompt templates.
* **Flask API:** Provides endpoints for sending and receiving messages.
* **CORS Support:** Enables cross-origin requests for frontend integration.
* **Error Handling:** Robust error handling for API requests and JSON parsing.

## Prerequisites

* Python 3.6+
* pip
* Hugging Face API token (set as an environment variable `HUGGINGFACE_API_TOKEN`)

## Installation

1.  **Clone the repository (if applicable):**
    ```bash
    git clone <repository_url>
    cd <repository_directory>
    ```

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    ```

3.  **Activate the virtual environment:**
    * **Windows:** `venv\Scripts\activate`
    * **macOS/Linux:** `source venv/bin/activate`

4.  **Install dependencies:**
    ```bash
    pip install Flask requests flask-cors
    ```

5.  **Set the Hugging Face API token:**
    * **Windows:** `set HUGGINGFACE_API_TOKEN=your_token`
    * **macOS/Linux:** `export HUGGINGFACE_API_TOKEN=your_token`

## Usage

1.  **Run the Flask application:**
    ```bash
    python agent.py
    ```

2.  **API Endpoint:**

    * `POST /send_message`: Sends a message to the AI agent and receives a response.

3.  **Request Body (JSON):**

    ```json
    {
      "message": "Your message here"
    }
    ```

4.  **Response (JSON):**

    ```json
    {
      "ai_response": "AI agent's response"
    }
    ```

## Configuration

* **Hugging Face Model:**
    * Modify the `HUGGINGFACE_API_URL` variable in `agent.py` to use a different Hugging Face model.
* **Prompt Template:**
    * Customize the prompt template in the `generate_response()` function to adjust the AI agent's behavior.
* **Conversation History Length:**
    * Adjust the `if len(conversation_history) > 10:` condition in `generate_response()` to control the length of the conversation history.

## Error Handling

* The application includes error handling for API requests and JSON parsing.
* Error messages are printed to the console for debugging purposes.

## Dependencies

* **Flask:** Web framework for building the API.
* **requests:** HTTP library for making API requests to Hugging Face.
* **flask-cors:** Extension for handling Cross-Origin Resource Sharing.
* **os:** For accessing environment variables.
* **json:** Used for handling JSON data.
* **time:** Used to add delays between API calls.

## Notes

* Ensure that the Hugging Face API token is set correctly as an environment variable.
* Be aware of the Hugging Face Inference API's usage limits.
* The conversation history is stored in memory and will be lost when the application is restarted.
* The model used for the API calls can be changed by modifying the `HUGGINGFACE_API_URL` variable.
* The prompt can be changed to customize the agent's behaviour.