#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# pip install keyboard
import keyboard


def print_pressed_keys(e) -> None:
    print(e, e.event_type, e.name)


keyboard.hook(print_pressed_keys)
keyboard.wait()
