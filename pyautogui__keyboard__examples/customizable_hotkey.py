#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# SOURCE: https://github.com/boppreh/keyboard/blob/master/examples/customizable_hotkey.py


# pip install keyboard
import keyboard


print("Press and release your desired shortcut: ")

shortcut = keyboard.read_shortcut()
print("Shortcut selected:", shortcut)


def on_triggered():
    print("Triggered!")


keyboard.add_hotkey(shortcut, on_triggered)

print("Press ESC to stop.")
keyboard.wait("esc")
