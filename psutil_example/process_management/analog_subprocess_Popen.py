#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# pip install psutil
import psutil
from subprocess import PIPE

p = psutil.Popen(["python", "-c", "print('hello')\nprint('world!')"], stdout=PIPE)
print(p.name())
print(p.username())
print(p.communicate())
print(p.wait(timeout=2))
