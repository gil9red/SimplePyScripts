#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# https://ru.wikipedia.org/wiki/Переменная_среды_Windows

import os


app_data = os.path.expandvars("%APPDATA%")
print(app_data)
print()

print(os.path.expandvars("%OS%"))
print(os.path.expandvars("%COMPUTERNAME%"))
print(os.path.expandvars("%WINDIR%"))
print()

print(os.path.expandvars("%NUMBER_OF_PROCESSORS%"))
print(os.path.expandvars("%PROCESSOR_ARCHITECTURE%"))
