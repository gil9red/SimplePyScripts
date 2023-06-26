#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://docs.python.org/3/library/shutil.html#archiving-operations


import shutil


print("Archive formats:")
for i, (name, description) in enumerate(shutil.get_archive_formats(), 1):
    print(f'  {i}. {name}: "{description}"')

print()

print("Unpack formats:")
for i, (name, extensions, description) in enumerate(shutil.get_unpack_formats(), 1):
    print(f'  {i}. {name}, {extensions}: "{description}"')
