#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import ctypes


# SOURCE: https://docs.microsoft.com/ru-ru/windows/desktop/api/winuser/nf-winuser-messagebeep
#
# BOOL MessageBeep(
#   UINT uType
# );
MessageBeep = ctypes.windll.user32.MessageBeep


ok = MessageBeep(0xFFFFFFFF)
print(ok)
