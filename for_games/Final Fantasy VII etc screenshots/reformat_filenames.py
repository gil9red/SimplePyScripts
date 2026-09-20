#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import re
from pathlib import Path

FILE_PATTERN: re.Pattern = re.compile(r"^(\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2})-\d+ \((\d+)\)$")

# NOTE: "2026-09-17_04-34-08-647679 (1).png" -> "2026-09-17_04-34-08-000001.png"
# NOTE: "2026-09-17_04-34-08-647679 (2).jpg" -> "2026-09-17_04-34-08-000002.jpg"
for path in Path(r"C:\Users\ipetrash\Desktop\FF7 Screenshots").rglob("*.*"):
    if not path.is_file():
        continue

    m: re.Match | None = FILE_PATTERN.match(path.stem)
    if not m:
        continue

    new_name: str = f"{m.group(1)}-{m.group(2).zfill(6)}{path.suffix}"

    new_path: Path = path.parent / new_name
    if path.name == new_path.name:
        continue

    print(f'Renaming "{path}" to "{new_path.name}"')
    path.rename(new_path)
