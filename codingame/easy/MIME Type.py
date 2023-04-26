#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import sys


# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

ext_mime_dict = dict()
files = list()

n = int(input())  # Number of elements which make up the association table.
q = int(input())  # Number Q of file names to be analyzed.
for i in range(n):
    # ext: file extension
    # mt: MIME type.
    ext, mt = input().split()
    ext_mime_dict[ext.lower()] = mt

for i in range(q):
    fname = input()  # One file name per line.
    files.append(fname)

print(ext_mime_dict, file=sys.stderr)
print(files, file=sys.stderr)

# Write an action using print
# To debug: print("Debug messages...", file=sys.stderr)

# For each of the Q filenames, display on a line the corresponding MIME type. If there is no corresponding
# type, then display UNKNOWN.

for file in files:
    try:
        i = file.rindex(".")
        ext = file[i + 1 :].lower()
        print(ext_mime_dict[ext])
    except:
        print("UNKNOWN")
