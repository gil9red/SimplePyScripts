#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import time
import os


def shutdown(off_pc=19):
    while time.localtime().tm_hour != off_pc:
        time.sleep(60)  # Ожидание 1 минута
        
    ## os.system("shutdown -s")
    # import sys
    #
    # if sys.platform == 'win32':
    #
    #     import ctypes
    #     user32 = ctypes.WinDLL('user32')
    #     user32.ExitWindowsEx(0x00000008, 0x00000000)
    #
    # else:
    #
    #     import os
    #     os.system('sudo shutdown now')
    #
    print("shutdown -s")


if __name__ == '__main__':
    shutdown()
