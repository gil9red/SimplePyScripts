#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from pathlib import Path

from PyQt6.QtCore import QFile

PATH: Path = Path(__file__).resolve()
DIR: Path = PATH.parent

PATH_EXAMPLE: Path = DIR / f"{PATH.name}.txt"
PATH_EXAMPLE.write_text("Hello World!")

print(f"Writing to file '{PATH_EXAMPLE.name}'")

file_path: str = str(PATH_EXAMPLE)
file_obj: QFile = QFile(file_path)
if file_obj.moveToTrash():
    print(f"File '{file_path}' was successfully moved to trash.")
else:
    print(f"Failed to move file '{file_path}' to trash.")
