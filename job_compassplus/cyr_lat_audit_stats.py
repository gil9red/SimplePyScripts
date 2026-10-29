#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import re
from collections import Counter
from pathlib import Path

# TODO:
file_path: str = r"C:\Users\IPetrash\Desktop\cyr_lat_audit.py-v9.txt"

text = Path(file_path).read_text("utf-8")
items = re.findall("File: '(.+?)'", text)
print(items)

module_counter: Counter[str] = Counter()
for item in items:
    module_counter[item.split("\\\\")[4] + "/" + item.split("\\\\")[5].split(".")[0]] += 1
print(module_counter)
for module, count in module_counter.most_common():
    print(f"{module}: {count}")
