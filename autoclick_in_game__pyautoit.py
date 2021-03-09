#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import threading
import time

import keyboard

# pip install PyAutoIt
import autoit


DATA = {
    'START': False,
}


def change_start():
    DATA['START'] = not DATA['START']
    print(DATA['START'])


def process_auto_click():
    while True:
        if not DATA['START']:
            time.sleep(0.100)
            continue

        # Симуляция атаки
        if DATA['START']:
            autoit.mouse_click()

        time.sleep(0.070)


keyboard.add_hotkey('Ctrl+Alt+Space', change_start)

# Запуск потока для автоатаки
thread_auto_click = threading.Thread(target=process_auto_click)
thread_auto_click.start()


while True:
    if not DATA['START']:
        time.sleep(0.100)
        continue
