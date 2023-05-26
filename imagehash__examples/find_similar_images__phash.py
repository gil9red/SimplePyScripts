#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://github.com/JohannesBuchner/imagehash


import itertools
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

print("Find similar images")

for img_1, img_2 in itertools.combinations(img_by_hash.items(), 2):
    file_name_1, hash_img_1 = img_1
    file_name_2, hash_img_2 = img_2

    score = hash_img_1 - hash_img_2
    if score > 10:
        continue

    print(f'Score: {score:2}. Similar images: "{file_name_1}" and "{file_name_2}"')
