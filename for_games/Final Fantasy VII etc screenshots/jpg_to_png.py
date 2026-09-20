#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from pathlib import Path


for path in Path(r"C:\Users\ipetrash\Desktop\FF7 Screenshots").rglob("*.*"):
    if not path.is_file():
        continue

    if path.suffix.lower() not in [".jpg", ".jpeg"]:
        continue

    new_name: str = f"{path.stem}.png"

    new_path: Path = path.parent / new_name
    if path.name == new_path.name:
        continue

    print(f'Renaming "{path}" to "{new_path.name}"')
    path.rename(new_path)

