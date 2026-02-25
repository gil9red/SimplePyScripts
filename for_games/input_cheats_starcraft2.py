#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# Запустить скрипт от админа. В игре: нажать Enter, ввести комбинацию для чита, нажать Ctrl+V


import os

# pip install keyboard
import keyboard


def write(text: str) -> None:
    print(text)

    os.system(f"echo {text}|clip")


# Отключение тумана войны
keyboard.add_hotkey("Ctrl+Shift+Z", write, args=["TookTheRedPill"])

# +5000 к каждому ресурсу
keyboard.add_hotkey("Ctrl+Shift+X", write, args=["WhoRunBartertown"])

# Активация быстрой постройки и улучшений
keyboard.add_hotkey("Ctrl+Shift+C", write, args=["CatFoodForPrawnGuns"])

# Режим «бога»
keyboard.add_hotkey("Ctrl+Shift+V", write, args=["TerribleTerribleDamage"])

# Мгновенная победа
keyboard.add_hotkey("Ctrl+Shift+B", write, args=["WhatIsBestInLife"])

keyboard.wait()
