#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


def shutdown(off_pc=19):
    import time

    while time.localtime().tm_hour != off_pc:
        time.sleep(60)  # Ожидание 1 минута

    import sys

    if sys.platform == 'win32':
        import ctypes
        user32 = ctypes.WinDLL('user32')

        # https://docs.microsoft.com/en-us/windows/desktop/api/winuser/nf-winuser-exitwindowsex
        EWX_POWEROFF = 0x00000008
        user32.ExitWindowsEx(EWX_POWEROFF, 0x00000000)

    else:
        import os
        os.system('sudo shutdown now')


if __name__ == '__main__':
    shutdown()
