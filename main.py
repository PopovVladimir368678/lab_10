import json, os

import pyttsx3, pyaudio, vosk
import requests



tts = pyttsx3.init('sapi5')


voices = tts.getProperty('voices')
tts.setProperty('voices', 'ru')

for voice in voices:
    print(voice.name)
    if voice.name == 'Irina':
        tts.setProperty('voice', voice.id)

model = vosk.Model('vosk-model-small-ru-0.4')
record = vosk.KaldiRecognizer(model, 16000)
pa = pyaudio.PyAudio()
stream = pa.open(format=pyaudio.paInt16,
                 channels=1,
                 rate=16000,
                 input=True,
                 frames_per_buffer=8000)
stream.start_stream()


def listen():
    while True:
        data = stream.read(4000, exception_on_overflow=False)
        if record.AcceptWaveform(data) and len(data) > 0:
            answer = json.loads(record.Result())
            if answer['text']:
                yield answer['text']


def speak(say):
    tts.say(say)
    tts.runAndWait()


speak('Я тут, можно начинать работать')
print('start...')
for text in listen():
    if text == 'закрыть':
        quit()
    elif text == 'прочитай текст':
        URL_TEMPLATE = "https://loripsum.net/api/10/short/headers"
        r = requests.get(URL_TEMPLATE)
        speak(r.text)

    elif text == 'сохрани полностью':
        URL_TEMPLATE = "https://loripsum.net/api/10/short/headers"
        r = requests.get(URL_TEMPLATE)
        file = open("otus.txt", "w", encoding='utf-8')
        file.write(r.text)
        file.close()
        speak('сохранила')

    elif text == 'сохрани текст ':
        URL_TEMPLATE = "https://loripsum.net/api/10/short/headers"
        r = requests.get(URL_TEMPLATE)
        file = open("otus.html", "w", encoding='utf-8')
        file.write(r.text)
        file.close()
        speak('сохранила')


    elif text == 'выведи текст':
        URL_TEMPLATE = "https://loripsum.net/api/10/short/headers"
        r = requests.get(URL_TEMPLATE)
        print(r.text)

    else:
        print(text)