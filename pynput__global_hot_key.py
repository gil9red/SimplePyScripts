#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


if __name__ == '__main__':
    def on_release(key):
        if str(key) == 'Key.f7':
            print('screenshot')

            # Fullscreen
            import pyscreenshot as ImageGrab
            im = ImageGrab.grab()
            im.save('screenshot.png')
            im.show()

    from pynput import keyboard
    with keyboard.Listener(on_release=on_release) as listener:
        listener.join()
