#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from pathlib import Path


f = Path("~/test_file.txt").expanduser()
print(f.exists())  # False

print(f)  # C:\Users\ipetrash\test_file.txt
print(f.exists())  # False

print(f.write_text("Hello World", encoding="utf-8"))  # 11
print(f.exists())  # True

print(f.read_text(encoding="utf-8"))  # Hello World

print(f.unlink())  # None
print(f.exists())  # False
