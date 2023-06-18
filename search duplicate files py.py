#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import glob
import hashlib

from collections import defaultdict


all_file_name = glob.glob("**/*.py", recursive=True)
print("Total files:", len(all_file_name))

hash_by_files = defaultdict(list)

for file_name in all_file_name:
    with open(file_name, "rb") as f:
        hash_hex = hashlib.sha1(f.read()).hexdigest()

        hash_by_files[hash_hex].append(file_name)

print("Unique files:", len(hash_by_files))
print()

print("Duplicates:")
for hash_hex, files in hash_by_files.items():
    if len(files) == 1:
        continue

    print("    {} ({}):".format(hash_hex, len(files)))
    for file_name in files:
        print("        " + file_name)

    print()
