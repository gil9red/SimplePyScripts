#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# pip install pynput-1.8.1
from pynput.keyboard import Key, Listener

# pip install pyscreenshot
import pyscreenshot as ImageGrab


def on_release(key) -> None:
    if key == Key.f7:
        print("screenshot")

        # Fullscreen
        im = ImageGrab.grab()
        im.save("screenshot.png")
        im.show()


with Listener(on_release=on_release) as listener:
    listener.join()
