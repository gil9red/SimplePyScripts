#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import winreg


# SOURCE: https://docs.python.org/3/library/winreg.html#value-types
TYPE_BY_VALUE: dict[str, int] = {
    "REG_SZ": winreg.REG_SZ,
    "REG_EXPAND_SZ": winreg.REG_EXPAND_SZ,
    "REG_BINARY": winreg.REG_BINARY,
    "REG_DWORD": winreg.REG_DWORD,
    "REG_MULTI_SZ": winreg.REG_MULTI_SZ,
    "REG_QWORD": winreg.REG_QWORD,
    "REG_NONE": winreg.REG_NONE,
    "REG_DWORD_BIG_ENDIAN": winreg.REG_DWORD_BIG_ENDIAN,
    "REG_LINK": winreg.REG_LINK,
    "REG_RESOURCE_LIST": winreg.REG_RESOURCE_LIST,
    "REG_FULL_RESOURCE_DESCRIPTOR": winreg.REG_FULL_RESOURCE_DESCRIPTOR,
    "REG_RESOURCE_REQUIREMENTS_LIST": winreg.REG_RESOURCE_REQUIREMENTS_LIST,
}
VALUE_BY_TYPE: dict[int, str] = {v: k for k, v in TYPE_BY_VALUE.items()}
