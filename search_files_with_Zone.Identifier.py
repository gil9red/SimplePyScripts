#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://blogs.technet.microsoft.com/askcore/2013/03/24/alternate-data-streams-in-ntfs/


import subprocess

from glob import glob
from os.path import isfile, expanduser, normpath


# Example: 'C:/Users/<user_name>/Downloads'
DIR_NAME = normpath(expanduser("~/Downloads"))

print(f'Search in "{DIR_NAME}"\n')


# NOTE: For test
f = open("log.txt", "w", encoding="utf-8")

# For statistic
files = [
    file_name
    for file_name in glob(DIR_NAME + "/**/*", recursive=True)
    if isfile(file_name)
]
found = 0

for i, file_name in enumerate(files, 1):
    print(f"{i}/{len(files)} ({int(i / len(files) * 100)}%). found: {found}")

    escape_file_name = file_name.replace("[", "`[").replace("]", "`]")
    try:
        cmd = f'''powershell -Command "get-content '{escape_file_name}' -stream Zone.Identifier"'''
        # print(cmd)

        text = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
        print("  [+]", file_name, text)
        f.write(file_name + " " + repr(text) + "\n")
        found += 1

    # NOTE: for test
    except subprocess.CalledProcessError as e:
        data = e.output
        print("  [-]", file_name, e, repr(data.decode("cp1251")))
