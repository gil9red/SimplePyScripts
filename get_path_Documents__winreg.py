#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from winreg import *


aReg = ConnectRegistry(None, HKEY_CURRENT_USER)
aKey = OpenKey(
    aReg, r"Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders"
)
name = QueryValueEx(aKey, "Personal")[0]
print(name)
# C:\Users\ipetrash\Documents
