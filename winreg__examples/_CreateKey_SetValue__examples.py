#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import winreg

key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 'Software')
winreg.CreateKey(key, 'SAMP')
winreg.CloseKey(key)

key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 'Software\\SAMP')
winreg.SetValue(key, 'PlayerName', winreg.REG_SZ, "Simon")
winreg.CloseKey(key)

keyValue = 'Software\\SAMP\\PlayerName'
key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, keyValue, 0, winreg.KEY_ALL_ACCESS)
winreg.SetValueEx(key, 'Name', None, winreg.REG_SZ, "SimonSimon")

winreg.CloseKey(key)
