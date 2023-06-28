#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://gist.github.com/wontoncc/1808234
#
# Analog: https://github.com/K-DawG007/Stack-Watch/blob/master/windows_popup.py
# Analog: https://github.com/jithurjacob/Windows-10-Toast-Notifications


import sys
import os
import time
import uuid

import win32con
from win32gui import *


class WindowsBalloonTip:
    @staticmethod
    def balloon_tip(title, msg, duration=5, icon_path_name=None):
        message_map = {
            win32con.WM_DESTROY: WindowsBalloonTip.on_destroy,
        }

        # Register the Window class.
        wc = WNDCLASS()
        hinst = wc.hInstance = GetModuleHandle(None)

        # Random class name
        wc.lpszClassName = str(uuid.uuid1())
        wc.lpfnWndProc = message_map  # could also specify a wndproc.

        class_atom = RegisterClass(wc)

        # Create the Window.
        style = win32con.WS_OVERLAPPED | win32con.WS_SYSMENU
        hwnd = CreateWindow(
            class_atom,
            "Taskbar",
            style,
            0,
            0,
            win32con.CW_USEDEFAULT,
            win32con.CW_USEDEFAULT,
            0,
            0,
            hinst,
            None,
        )
        UpdateWindow(hwnd)

        if not icon_path_name:
            icon_path_name = os.path.abspath(
                os.path.join(sys.path[0], "balloontip.ico")
            )

        icon_flags = win32con.LR_LOADFROMFILE | win32con.LR_DEFAULTSIZE
        try:
            hicon = LoadImage(
                hinst, icon_path_name, win32con.IMAGE_ICON, 0, 0, icon_flags
            )
        except:
            hicon = LoadIcon(0, win32con.IDI_APPLICATION)

        flags = NIF_ICON | NIF_MESSAGE | NIF_TIP
        nid = (hwnd, 0, flags, win32con.WM_USER + 20, hicon, "tooltip")
        Shell_NotifyIcon(NIM_ADD, nid)
        Shell_NotifyIcon(
            NIM_MODIFY,
            (
                hwnd,
                0,
                NIF_INFO,
                win32con.WM_USER + 20,
                hicon,
                "Balloon  tooltip",
                msg,
                200,
                title,
            ),
        )

        time.sleep(duration)

        DestroyWindow(hwnd)
        UnregisterClass(wc.lpszClassName, None)

    @staticmethod
    def on_destroy(hwnd, msg, wparam, lparam):
        nid = (hwnd, 0)
        Shell_NotifyIcon(NIM_DELETE, nid)
        PostQuitMessage(0)  # Terminate the app.


if __name__ == "__main__":
    WindowsBalloonTip.balloon_tip("First", "My Text!", duration=2)
    WindowsBalloonTip.balloon_tip("Second", "My NEW Text!", duration=3)
    WindowsBalloonTip.balloon_tip(
        "Three", "With invalid icons!", icon_path_name="fdfs.ico"
    )
