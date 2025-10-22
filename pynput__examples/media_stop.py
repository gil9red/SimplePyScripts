#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# pip install pynput-1.8.1
from pynput.keyboard import Key, Controller


keyboard = Controller()

print("Attempting to stop media playback using pynput...")

keyboard.press(Key.media_stop)
keyboard.release(Key.media_stop)

print("Media stop command sent via pynput.")
