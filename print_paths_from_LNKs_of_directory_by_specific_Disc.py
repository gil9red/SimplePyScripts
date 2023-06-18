#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import os
from glob import iglob

# pip install winshell
import winshell


path_desktop_lnk = os.path.expanduser(r"~\Desktop\Пройти\*.lnk")
need_disc = "E:"

paths = []

for file_name in iglob(path_desktop_lnk):
    shortcut = winshell.shortcut(file_name)
    path = shortcut.path
    if path.startswith(need_disc):
        paths.append(path)

paths.sort()

print(f"Total lnk's on {need_disc!r} ({len(paths)}):")
for i, path in enumerate(paths, 1):
    print(f"{i:3}. {path}")
