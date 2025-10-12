#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import ctypes
import sys

from is_user_admin import is_user_admin


if not is_user_admin():
    # TODO: Поддержка не в Windows
    # Перезапускаем скрипт с правами админа
    ctypes.windll.shell32.ShellExecuteW(
        None, "runas", sys.executable, __file__, None, 1
    )
    sys.exit()

print("Your code...")

# Если админ продолжаем скрипт дальше
print("admin!!!")

input()
