
import requests
import urllib.parse
from scripts.katakana import *

 
def voicevox_tts(tts):
    
    voicevox_url = 'http://localhost:50021'
    katakana_text = katakana_converter(tts)
    params_encoded = urllib.parse.urlencode({'text': katakana_text, 'speaker': 20})
    request = requests.post(f'{voicevox_url}/audio_query?{params_encoded}')
    params_encoded = urllib.parse.urlencode({'speaker': 20, 'enable_interrogative_upspeak': True})
    request = requests.post(f'{voicevox_url}/synthesis?{params_encoded}', json=request.json())

    with open("test.wav", "wb") as outfile:
        outfile.write(request.content)


