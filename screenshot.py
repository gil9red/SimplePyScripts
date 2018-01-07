#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


if __name__ == "__main__":
    # fullscreen
    import pyscreenshot as ImageGrab
    im = ImageGrab.grab()
    im.save('screenshot.png')
    im.show()
