
import sys
import googletrans
import deepl
from config import *
sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf8', buffering=1)


def translate_deepl(text,source,target):
    authkey = auth_key 
    translator = deepl.Translator(authkey)

    result = translator.translate_text(text, source_lang=source, target_lang=target)
    return result.text


def translate_google(text, source, target):
    try:
        translator = googletrans.Translator()
        result = translator.translate(text, src=source, dest=target)
        return result.text
    except:
        print("Error translate")
        return
    
def detect_google(text):
    try:
        translator = googletrans.Translator()
        result = translator.detect(text)
        return result.lang.upper()
    except:
        print("Error detect")
        return

