#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# pip install keyboard
import keyboard


keyboard.press_and_release("tab, tab, tab")

keyboard.write("The quick brown fox jumps over the lazy dog.")

# Press PAGE UP then PAGE DOWN to type "foobar".
keyboard.add_hotkey("page up, page down", lambda: keyboard.write("foobar"))

# Blocks until you press esc.
keyboard.wait("esc")

# Record events until 'esc' is pressed.
recorded = keyboard.record(until="esc")

# Then replay back at three times the speed.
keyboard.play(recorded, speed_factor=3)

# Type @@ then press space to replace with abbreviation.
keyboard.add_abbreviation("@@", "my.long.email@example.com")

# Block forever.
keyboard.wait()
