#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import time
import os
from threading import Thread

# pip install PyAutoIt==0.6.5
import autoit

# pip install keyboard==0.13.5
import keyboard


DATA = {
    "START": False,
}

HOTKEY: str = os.environ.get("HOTKEY", "Ctrl+Alt+Space")


def change_start():
    DATA["START"] = not DATA["START"]
    print("START:", DATA["START"])


def process_auto_click():
    while True:
        if not DATA["START"]:
            time.sleep(0.100)
            continue

        # Симуляция атаки
        if DATA["START"]:
            autoit.mouse_click()

        time.sleep(0.070)


keyboard.add_hotkey(HOTKEY, change_start)

# Запуск потока для автоатаки
thread_auto_click = Thread(target=process_auto_click)
thread_auto_click.start()


print(f"Press {HOTKEY} for starting/stopping")

while True:
    if not DATA["START"]:
        time.sleep(0.100)
        continue
