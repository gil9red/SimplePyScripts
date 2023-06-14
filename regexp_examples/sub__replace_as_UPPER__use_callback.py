#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import re


text = "Hello World! Mega tetris +100500! Привет мир!"
new_text = re.sub(r"\w+", lambda x: x[0].upper(), text)
print(new_text)  # HELLO WORLD! MEGA TETRIS +100500! ПРИВЕТ МИР!
