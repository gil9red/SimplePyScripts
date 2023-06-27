#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# NOTE: this example requires PyAudio because it uses the Microphone class

# pip install pyaudio
# pip install SpeechRecognition
import speech_recognition as sr


# obtain audio from the microphone
r = sr.Recognizer()
with sr.Microphone() as source:
    print("Say something!")
    audio = r.listen(source)

# write audio to a RAW file
with open("microphone-results.raw", "wb") as f:
    f.write(audio.get_raw_data())

# write audio to a WAV file
with open("microphone-results.wav", "wb") as f:
    f.write(audio.get_wav_data())

# write audio to an AIFF file
with open("microphone-results.aiff", "wb") as f:
    f.write(audio.get_aiff_data())

# write audio to a FLAC file
with open("microphone-results.flac", "wb") as f:
    f.write(audio.get_flac_data())
