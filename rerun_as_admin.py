#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import ctypes
import sys


def is_admin():
    """ Проверяем права"""
    try:
        # Если админ вернет True
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


if not is_admin():
    # Перезапускаем скрипт с правами админа
    ctypes.windll.shell32.ShellExecuteW(
        None, "runas", sys.executable,
        __file__, None, 1
    )
    sys.exit()

print("your code...")

# Если админ продолжаем скрипт дальше
print("admin!!!")

input()
