#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import time
import sys
import os


def shutdown(off_pc=19):
    while time.localtime().tm_hour != off_pc:
        time.sleep(60)  # Ожидание 1 минута

    if sys.platform == "win32":
        import ctypes
        import win32security
        import win32api
        import winerror

        # Try to enable the required privileges to change the power state
        privilege_flags = (
            win32security.TOKEN_ADJUST_PRIVILEGES | win32security.TOKEN_QUERY
        )
        token_handle = win32security.OpenProcessToken(
            win32api.GetCurrentProcess(), privilege_flags
        )
        privilege_id = win32security.LookupPrivilegeValue(
            None, win32security.SE_SHUTDOWN_NAME
        )

        # Does the user have permission to change the power state?
        win32security.AdjustTokenPrivileges(
            token_handle, 0, [(privilege_id, win32security.SE_PRIVILEGE_ENABLED)]
        )

        if ctypes.GetLastError() != winerror.ERROR_SUCCESS:
            print(ctypes.WinError(), file=sys.stderr)
            sys.exit()

        user32 = ctypes.WinDLL("user32")

        # https://docs.microsoft.com/en-us/windows/desktop/api/winuser/nf-winuser-exitwindowsex
        user32.ExitWindowsEx(0x00000001, 0x00000000)

        if ctypes.GetLastError() != winerror.ERROR_SUCCESS:
            print(ctypes.WinError(), file=sys.stderr)
            sys.exit()

    else:
        os.system("sudo shutdown now")


if __name__ == "__main__":
    shutdown()
