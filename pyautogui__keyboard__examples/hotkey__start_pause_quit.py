#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import time
import os

import keyboard


RUN_COMBINATION = "Ctrl+Shift+R"
QUIT_COMBINATION = "Ctrl+Shift+Q"
AUTO_ATTACK_COMBINATION = "Ctrl+Shift+Space"

BOT_DATA = {
    "START": False,
    "AUTO_ATTACK": False,
}


def change_start():
    BOT_DATA["START"] = not BOT_DATA["START"]
    print("START:", BOT_DATA["START"])


def change_auto_attack():
    BOT_DATA["AUTO_ATTACK"] = not BOT_DATA["AUTO_ATTACK"]
    print("AUTO_ATTACK:", BOT_DATA["AUTO_ATTACK"])


print('Press "{}" for RUN / PAUSE'.format(RUN_COMBINATION))
print('Press "{}" for QUIT'.format(QUIT_COMBINATION))
print('Press "{}" for AUTO_ATTACK'.format(AUTO_ATTACK_COMBINATION))


keyboard.add_hotkey(QUIT_COMBINATION, lambda: print("Quit by Escape") or os._exit(0))
keyboard.add_hotkey(AUTO_ATTACK_COMBINATION, change_auto_attack)
keyboard.add_hotkey(RUN_COMBINATION, change_start)

print("Start")

i = 1

while True:
    if not BOT_DATA["START"]:
        time.sleep(0.1)
        continue

    print(i, "AUTO_ATTACK:", BOT_DATA["AUTO_ATTACK"])

    time.sleep(1)
    i += 1
