#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://github.com/JohannesBuchner/imagehash


import itertools

from collections import defaultdict
from glob import glob

# pip install imagehash
import imagehash

# pip install pillow
from PIL import Image


file_names = glob(r"D:\все фотки\**\*.jpg", recursive=True)
print(f"Files: {len(file_names)}")

img_by_hash = dict()

for file_name in file_names:
    try:
        hash_img = imagehash.phash(Image.open(file_name))
    except Exception as e:
        print(f'Problem: {e} with "{file_name}"')
        continue

    img_by_hash[file_name] = hash_img

print("\nFind similar images")

file_name_by_similars = defaultdict(list)

for img_1, img_2 in itertools.product(img_by_hash.items(), repeat=2):
    if img_1 == img_2:
        continue

    file_name_1, hash_img_1 = img_1
    file_name_2, hash_img_2 = img_2

    score = hash_img_1 - hash_img_2
    if score > 10:
        continue

    file_name_by_similars[file_name_1].append(file_name_2)

# Обратная сортировка по количеству элементов
items = sorted(file_name_by_similars.items(), key=lambda x: len(x[1]), reverse=True)
i = 0
for file_name, similars in items:
    if not similars:
        continue

    i += 1
    print(f'{i}. "{file_name}" ({len(similars)}):')

    for j, x in enumerate(similars, 1):
        print(f'    {j}. "{x}"')

    print()
