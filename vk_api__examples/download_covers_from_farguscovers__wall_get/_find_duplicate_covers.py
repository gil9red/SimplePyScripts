#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import hashlib

from collections import defaultdict
from pathlib import Path

from main import DIR_IMAGES


def get_file_digest(file_name: Path) -> str:
    data = file_name.read_bytes()
    return hashlib.sha1(data).hexdigest()


hash_by_files = defaultdict(list)
for file_name in DIR_IMAGES.glob('*.jpg'):
    hash_by_files[get_file_digest(file_name)].append(file_name)

print('Duplicates:')
for file_names in hash_by_files.values():
    if len(file_names) == 1:
        continue

    file_names.sort(
        key=lambda x: int(''.join(c for c in x.name if c.isdigit()))
    )

    for file_name in file_names:
        rel_file_name = file_name.relative_to(DIR_IMAGES)
        print(f'    {rel_file_name}')

    print()
