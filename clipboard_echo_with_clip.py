#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import os
from tkinter import Tk  # Python 3


os.system("echo 123|clip")

print(repr(Tk().clipboard_get()))
# '123\n'
