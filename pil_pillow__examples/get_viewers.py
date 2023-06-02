#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from PIL.ImageShow import _viewers


print(f"Viewers: {len(_viewers)}")
for viewer in _viewers:
    print(viewer.get_command("123.png"))

"""
Viewers: 1
start "Pillow" /WAIT "123.png" && ping -n 2 127.0.0.1 >NUL && del /f "123.png"
"""
