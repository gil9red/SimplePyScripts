#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# pip install pynput
from pynput.keyboard import Key, Listener


def on_release(key):
    if key == Key.f7:
        print('screenshot')

        # Fullscreen
        import pyscreenshot as ImageGrab
        im = ImageGrab.grab()
        im.save('screenshot.png')
        im.show()


with Listener(on_release=on_release) as listener:
    listener.join()
