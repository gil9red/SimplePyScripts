#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import ctypes


# SOURCE: https://docs.microsoft.com/en-us/windows/desktop/api/Winuser/nf-winuser-messagebox


# int MessageBox(
#   HWND    hWnd,
#   LPCTSTR lpText,
#   LPCTSTR lpCaption,
#   UINT    uType
# );

MessageBox = ctypes.windll.user32.MessageBoxW


MB_ICONWARNING = 0x00000030
MB_CANCELTRYCONTINUE = 0x00000006
MB_DEFBUTTON2 = 0x00000100

IDCANCEL = 2
IDTRYAGAIN = 10
IDCONTINUE = 11


button_id = MessageBox(
    None,
    "Resource not available\nDo you want to try again?",
    "Account Details",
    MB_ICONWARNING | MB_CANCELTRYCONTINUE | MB_DEFBUTTON2,
)
print("button_id:", button_id)

if button_id == IDCANCEL:
    print("IDCANCEL")

elif button_id == IDTRYAGAIN:
    print("IDTRYAGAIN")

elif button_id == IDCONTINUE:
    print("IDCONTINUE")
