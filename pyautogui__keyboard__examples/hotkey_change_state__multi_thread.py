#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import time
import threading
import os

import keyboard


RUN_COMBINATION = "Ctrl+Shift+R"
QUIT_COMBINATION = "Ctrl+Shift+T"
AUTO_ATTACK_COMBINATION = "Ctrl+Shift+Space"

BOT_DATA = {
    "AUTO_ATTACK": False,
}


def change_auto_attack():
    BOT_DATA["AUTO_ATTACK"] = not BOT_DATA["AUTO_ATTACK"]
    print("AUTO_ATTACK:", BOT_DATA["AUTO_ATTACK"])


print('Press "{}" for RUN'.format(RUN_COMBINATION))
print('Press "{}" for QUIT'.format(QUIT_COMBINATION))
print('Press "{}" for AUTO_ATTACK'.format(AUTO_ATTACK_COMBINATION))


keyboard.add_hotkey(QUIT_COMBINATION, lambda: print("Quit by Escape") or os._exit(0))
keyboard.add_hotkey(AUTO_ATTACK_COMBINATION, change_auto_attack)
keyboard.wait(RUN_COMBINATION)

print("Start")


def process_auto_attack():
    i = 1

    while True:
        print(i, "AUTO_ATTACK:", BOT_DATA["AUTO_ATTACK"])

        time.sleep(1)
        i += 1


thread_auto_attack = threading.Thread(target=process_auto_attack)
thread_auto_attack.start()


i = 1

while True:
    print(i)

    time.sleep(1)
    i += 1
