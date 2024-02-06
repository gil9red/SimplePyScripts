#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import subprocess


PATH = r"HKLM:\HARDWARE\DESCRIPTION\System\CentralProcessor\0"
VALUE = "ProcessorNameString"

result: str = subprocess.check_output(rf'powershell -c "Get-ItemPropertyValue -Path {PATH} -Name {VALUE}"', encoding="utf-8")
value = result.strip()
print(value)
# Intel(R) Core(TM) i7-10750H CPU @ 2.60GHz
