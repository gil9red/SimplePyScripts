#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://github.com/nateshmbhat/pyttsx3


# pip install pyttsx3
import pyttsx3


engine = pyttsx3.init()  # Object creation

# RATE
rate = engine.getProperty("rate")  # Getting details of current speaking rate
print(rate)  # Printing current voice rate
engine.setProperty("rate", 125)  # Setting up new voice rate

# VOLUME
volume = engine.getProperty(
    "volume"
)  # Getting to know current volume level (min=0 and max=1)
print(volume)  # Printing current volume level
engine.setProperty("volume", 1.0)  # Setting up volume level  between 0 and 1

# VOICE
voices = engine.getProperty("voices")  # Getting details of current voice
# engine.setProperty('voice', voices[0].id)  # Changing index, changes voices. o for male
engine.setProperty(
    "voice", voices[1].id
)  # Changing index, changes voices. 1 for female

engine.say("Hello World!")
engine.say("My current speaking rate is " + str(rate))
engine.runAndWait()
engine.stop()
