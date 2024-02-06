#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import subprocess


PATH = r"HKLM\HARDWARE\DESCRIPTION\System\CentralProcessor\0"
VALUE = "ProcessorNameString"

# Example:
# "HKEY_LOCAL_MACHINE\HARDWARE\DESCRIPTION\System\CentralProcessor\0
#     ProcessorNameString    REG_SZ    Intel(R) Core(TM) i7-10750H CPU @ 2.60GHz"
result: str = subprocess.check_output(rf'Reg Query "{PATH}" /v {VALUE}', encoding="utf-8")

value = None
for line in result.splitlines():
    if VALUE in line:
        value = line.split("REG_SZ")[1].strip()
        break

print(value)
# Intel(R) Core(TM) i7-10750H CPU @ 2.60GHz
