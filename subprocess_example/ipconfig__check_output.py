#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import subprocess

try:
    text = subprocess.check_output(
        ["ipconfig"],
        stderr=subprocess.STDOUT,
    ).decode('cp866')

except subprocess.CalledProcessError as e:
    text = str(e)

print(text)
