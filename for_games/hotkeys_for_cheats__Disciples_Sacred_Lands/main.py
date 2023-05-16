#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# pip install keyboard
import keyboard


def input_command(text: str):
    keyboard.press_and_release("enter")

    keyboard.write(text)

    keyboard.press_and_release("enter")
    keyboard.press_and_release("esc")


HOTKEY_BY_COMMAND = {
    "U": "UPGRADEME",
    "G": "GIVEMEMONEY",
    "I": "IWANTTOBUILDAGAIN",
    "N": "NOWICANSEEYOU",
    "M": "MAKEMESTRONGER",
    "L": "LETMEMOVE",
    "R": "GIVEMEANOTHERCHANCE",
    "W": "NOBODYCANBEATME",
}

for hotkey, text in HOTKEY_BY_COMMAND.items():
    print(f"{hotkey}: {text}")
    keyboard.add_hotkey(hotkey, lambda text=text: input_command(text))

keyboard.wait()
