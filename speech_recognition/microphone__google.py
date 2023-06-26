#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# SOURCE: http://pythono.ru/speech-recognition-python/


# pip install pyaudio
# pip install SpeechRecognition
import speech_recognition as sr
r = sr.Recognizer()

with sr.Microphone() as source:
    print("Скажите что-нибудь")
    audio = r.listen(source)

try:
    text = r.recognize_google(audio, language="ru-RU")
    print(f'Фраза: "{text}"')

except sr.UnknownValueError:
    print("Робот не расслышал фразу")

except sr.RequestError as e:
    print(f"Ошибка сервиса: {e}")
