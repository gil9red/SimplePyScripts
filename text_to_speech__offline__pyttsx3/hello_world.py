#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://github.com/nateshmbhat/pyttsx3


# pip install pyttsx3
import pyttsx3


engine = pyttsx3.init()
engine.say("I will speak this text")
engine.runAndWait()
