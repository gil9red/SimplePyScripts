#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from collections import defaultdict
from pathlib import Path
from zlib import crc32


DIR = Path(r"C:\DOC\W4")

crc_by_files: dict[int, list[Path]] = defaultdict(list)
for f in DIR.rglob("*"):
    if not f.is_file():
        continue

    crc = crc32(f.read_bytes())
    crc_by_files[crc].append(f)

for files in crc_by_files.values():
    if len(files) == 1:
        continue

    print(*files, sep="\n")
    print()
