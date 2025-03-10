# Conversational AI Agent (Local, Free MVP) - Using Vosk

This project creates a basic conversational AI agent that interacts with the user via speech, utilizing entirely free and local resources. This setup is designed for development and proof-of-concept purposes, prioritizing cost-effectiveness over absolute accuracy. This version uses Vosk for offline Speech-to-Text.

## Features

* **Speech-to-Text (STT):** Uses Vosk for offline speech recognition.
* **Language Model (LLM):** Employs TinyLlama, a small, open-source language model, for generating responses.
* **Text-to-Speech (TTS):** Uses pyttsx3 for converting text responses to speech.

## Prerequisites

* **Python 3.x:** Download and install from [python.org](https://www.python.org/).
* **Vosk Language Model:** Downloaded from the Vosk website.
* **TinyLlama Model:** Downloaded automatically by the script, or manually from Hugging Face.
* **Microphone:** Properly connected and configured.

## Installation

1.  **Clone the Repository (Optional):**
    ```bash
    git clone <repository_url>
    cd <repository_directory>
    ```

2.  **Create a Virtual Environment (Recommended):**
    ```bash
    python -m venv venv
    ```
    * **Activate:**
        * Windows: `venv\Scripts\activate`
        * macOS/Linux: `source venv/bin/activate`

3.  **Install Python Libraries:**
    ```bash
    pip install vosk pyaudio transformers torch pyttsx3
    ```
    * **PyAudio Installation Notes:**
        * **Windows:** If `pip install pyaudio` fails, you might need to install a pre-built wheel.
            * Determine your Python version (`python --version`).
            * Download the appropriate `.whl` file from [https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio).
            * Install using: `pip install <filename.whl>` (replace `<filename.whl>` with the actual filename).
        * **macOS:** If you are using homebrew, run:
            ```bash
            brew install portaudio
            pip install pyaudio
            ```
        * **Linux (Debian/Ubuntu):**
            ```bash
            sudo apt-get install portaudio19-dev
            pip install pyaudio
            ```
        * **Linux (Fedora/CentOS/RHEL):**
            ```bash
            sudo yum install portaudio-devel
            pip install pyaudio
            ```
        * **Linux (Arch):**
            ```bash
            sudo pacman -S portaudio
            pip install pyaudio
            ```

4.  **Download Vosk Language Model:**

    * Go to the Vosk models page: [alphacephei.com/vosk/models](https://alphacephei.com/vosk/models).
    * Download the appropriate language model (e.g., `vosk-model-small-en-in-0.4`).
    * Extract the downloaded archive to a convenient location (e.g., `vosk-model-small-en-in-0.4`).

5.  **Download TinyLlama Model (Automatic or Manual):**

    * The model will be downloaded automatically the first time the script runs.
    * Alternatively, download it manually using the following Python code in a python interpreter:
        ```python
        from transformers import AutoTokenizer, AutoModelForCausalLM
        tokenizer = AutoTokenizer.from_pretrained("TinyLlama/TinyLlama-1.1B-Chat-v1.0")
        model = AutoModelForCausalLM.from_pretrained("TinyLlama/TinyLlama-1.1B-Chat-v1.0")
        ```

## Usage

1.  **Update the python script:**
    * You will need to update the python script to use Vosk instead of pocketsphinx. See the python code example in the previous conversation.
    * You will need to change the path to the vosk model in the python code.
2.  **Run the Python Script:**
    ```bash
    python agent.py
    ```

3.  **Speak into the Microphone:** The agent will listen, process your speech, and respond via synthesized voice.

## Troubleshooting

* **Vosk Errors:**
    * Verify the Vosk model path in your code.
    * Ensure the downloaded model is compatible with your system.
    * Verify that your microphone is working correctly.
* **PyTorch Errors:**
    * Verify PyTorch installation for your OS and hardware.
    * If you have a cuda enabled GPU, install the cuda version of pytorch.
* **Hugging Face Errors:**
    * Check internet connection and disk space.
    * Verify huggingface cache permissions.
* **Audio Issues:**
    * Check speaker and sound settings.
* **Poor STT Accuracy:**
    * Try different Vosk models.
    * Speak clearly in a quiet environment.

## Limitations

* **Accuracy:** The small LLM may result in lower accuracy compared to cloud-based solutions. Vosk accuracy is very good, but will vary depending on the model used.
* **Resource Usage:** Running the LLM locally requires CPU and RAM.
* **Voice Quality:** pyttsx3 provides basic voice synthesis.

## Future Improvements

* Fine-tune the LLM on specific domains.
* Explore noise reduction techniques for STT.
* Implement dialogue management for better conversation flow.
* Improve the audio output quality.