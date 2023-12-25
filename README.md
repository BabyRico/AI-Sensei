## Description

A virtual assistant/teacher that you can talk to your microphone. Has many features such as:

You can speak to her with a microphone
It can speak back to you
Has short-term memory and long-term memory
Fluent in Japanese
Custom identity

## AI Sensei & Assistant

This project implements various AI technologies such as VoiceVox Engine, DeepL, Whisper OpenAI, to create an AI assistant.

## Demo
 - [Demo](link here)


## Technologies Used

 - [VoiceVox Docker](https://hub.docker.com/r/voicevox/voicevox_engine)
 - [DeepL](https://www.deepl.com)
 - [Whisper OpenAI](https://platform.openai.com/account/api-keys)


## Installation

1. Install dependencies

```
pip install -r requirements.txt
```

2. Create config.py and store your Openai API key and DeepL Authentication key

```
api_key = 'apikey'
auth_key = 'authkey'
```

4. Set the identity of your assistant. Change the txt file at `characterConfig\Character\identity.txt`


In order to run the program using VoiceVox, you need to run VoiceVox Engine first. You can run it locally using [VoiceVox Docker](https://hub.docker.com/r/voicevox/voicevox_engine)


if you want to see the voice list of VoiceVox you can check this [VoiceVox](https://voicevox.hiroshiba.jp) and see the speaker id on `speaker.json` 

## Credits

This project is inspired by the work of Danu Kim and OneReality.

