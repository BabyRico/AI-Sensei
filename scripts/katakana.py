import romajitable
import sys

sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf8', buffering=1)


def katakana_converter(text):
    result = romajitable.to_kana(text)
    text = result.katakana

    return text