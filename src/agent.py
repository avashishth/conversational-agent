import vosk
import pyaudio
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import pyttsx3
import os

# Initialize Vosk
vosk.SetLogLevel(0)  # Suppress Vosk logs
model_path = "models/vosk-model-small-en-in-0.4"  # Replace with your Vosk model path
if not os.path.exists(model_path):
    print(f"Please download the Vosk model from alphacephei.com/vosk/models and place it in {model_path}")
    exit()

model = vosk.Model(model_path)
recognizer = vosk.KaldiRecognizer(model, 16000)

# Initialize PyAudio
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
stream.start_stream()

# Initialize LLM (TinyLlama example)
tokenizer = AutoTokenizer.from_pretrained("TinyLlama/TinyLlama-1.1B-Chat-v1.0")
llm_model = AutoModelForCausalLM.from_pretrained("TinyLlama/TinyLlama-1.1B-Chat-v1.0")

# Initialize TTS
engine = pyttsx3.init()

def speech_to_text():
    while True:
        data = stream.read(4000)
        if len(data) == 0:
            break
        if recognizer.AcceptWaveform(data):
            result = recognizer.Result()
            text = eval(result)["text"]
            if text:
                return text

def generate_response(user_input):
    inputs = tokenizer.encode(user_input, return_tensors="pt")
    outputs = llm_model.generate(inputs, max_length=100, do_sample=True)
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return response

def text_to_speech(text):
    engine.say(text)
    engine.runAndWait()

def main():
    print("Ready to listen...")
    while True:
        user_input = speech_to_text()
        if user_input:
            print(f"User: {user_input}")
            ai_response = generate_response(user_input)
            print(f"AI: {ai_response}")
            text_to_speech(ai_response)

if __name__ == "__main__":
    main()