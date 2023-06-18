#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import shutil
from pathlib import Path

# pip install winshell
import winshell


DIR = Path(r"~\Desktop\Пройти").expanduser()
DIR_NOT_EXISTENT = DIR / "Несуществуют"

files = []
for file_name in DIR.glob("*.lnk"):
    shortcut = winshell.shortcut(str(file_name))
    path = Path(shortcut.path)
    if not path.exists():
        files.append(file_name)

print(f"Найдено {len(files)}")

if files:
    DIR_NOT_EXISTENT.mkdir(parents=True, exist_ok=True)

    for f in files:
        print(f"Выполнено перемещение {f.name} в папку {DIR_NOT_EXISTENT}")

        new_file = DIR_NOT_EXISTENT / f.name
        shutil.move(f, new_file)
