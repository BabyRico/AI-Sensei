import openai
import winsound
import sys
import time
import pyaudio
import keyboard
import wave
import json
from config import *
from scripts.translate import *
from scripts.TTS import *
from scripts.promptMaker import *


# to help the CLI write unicode characters to the terminal
sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf8', buffering=1)

openai.api_key = api_key

conversation = []
# Create a dictionary to hold the message data
history = {"history": conversation}

total_characters = 0
chat = ""
chat_now = ""
chat_prev = ""
is_Speaking = False
owner_name = "イーサン"
# function to get input audio
def record_audio():
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 48000
    WAVE_OUTPUT_FILENAME = "input.wav"
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)
    frames = []
    print("Listening...")
    while keyboard.is_pressed('RIGHT_SHIFT'):
        data = stream.read(CHUNK)
        frames.append(data)
    print("Stopped Listening...")
    stream.stop_stream()
    stream.close()
    p.terminate()
    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    transcribe_audio("input.wav")

# function to transcribe the user's audio
def transcribe_audio(file):
    global chat_now
    try:
        audio_file= open(file, "rb")
        transcript = openai.Audio.transcribe("whisper-1", audio_file)
        chat_now = transcript.text
        print ("Question: " + chat_now)
    except Exception as e:
        print("Error transcribing audio: {0}".format(e))
        return

    result = owner_name + " said " + chat_now
    conversation.append({'role': 'user', 'content': result})
    openai_answer()

# function to get an answer from OpenAI
def openai_answer():
    global total_characters, conversation

    total_characters = sum(len(d['content']) for d in conversation)

    while total_characters > 4000:
        try:
            conversation.pop(2)
            total_characters = sum(len(d['content']) for d in conversation)
        except Exception as e:
            print("Error removing old messages: {0}".format(e))

    with open("conversation.json", "w", encoding="utf-8") as f:
        # Write the message data to the file in JSON format
        json.dump(history, f, indent=4)

    prompt = getPrompt()

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=prompt,
        max_tokens=128,
        temperature=1,
        top_p=0.9
    )
    message = response['choices'][0]['message']['content']
    conversation.append({'role': 'assistant', 'content': message})

    translate_text(message)

#function to translate message to desired language
def translate_text(text):
    global is_Speaking

    # tts will be the string to be converted to audio
    detect = detect_google(text)
    tts = translate_deepl(text, f"{detect}", "JA")
    tts_en = translate_deepl(text, f"{detect}", "EN-US")
    try:
        print("JP Answer: " + tts)
        print("EN Answer: " + tts_en)
    except Exception as e:
        print("Error printing text: {0}".format(e))
        return

    voicevox_tts(tts)


    # is_Speaking is used to prevent the assistant speaking more than one audio at a time
    is_Speaking = True
    winsound.PlaySound("test.wav", winsound.SND_FILENAME)
    is_Speaking = False

    # Clear text files after AI has finished speaking

    with open ("output.txt", "w") as f:
        f.truncate(0)
    with open ("chat.txt", "w") as f:
        f.truncate(0)

def preparation():
    global conversation, chat_now, chat, chat_prev
    while True:
        # If the assistant is not speaking, and the chat is not empty, and the chat is not the same as the previous chat
        # then the assistant will answer the chat
        chat_now = chat
        if is_Speaking == False and chat_now != chat_prev:
            # Save chat history
            conversation.append({'role': 'user', 'content': chat_now})
            chat_prev = chat_now
            openai_answer()
        time.sleep(1)

if __name__ == "__main__":
    try:
            print("Press and Hold Right Shift to record audio")
            while True:
                if keyboard.is_pressed('RIGHT_SHIFT'):
                    record_audio()

    except KeyboardInterrupt:
        print("Stopped")

