#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import os
from glob import glob

# pip install winshell
import winshell


path_desktop_lnk = os.path.expanduser(r"~\Desktop\**\*.lnk")

file_name = glob(path_desktop_lnk, recursive=True)[0]
shortcut = winshell.shortcut(file_name)
print(shortcut)
print(shortcut.lnk_filepath)
print(shortcut.path)
print(shortcut.working_directory)
