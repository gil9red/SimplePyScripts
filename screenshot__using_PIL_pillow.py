#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# Fullscreen
from PIL import ImageGrab
im = ImageGrab.grab()
im.save('screenshot.png')
im.show()
