#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import winreg


def get_reg(reg_path, name):
    try:
        with winreg.OpenKey(
            winreg.HKEY_CURRENT_USER, reg_path, 0, winreg.KEY_READ
        ) as registry_key:
            value, regtype = winreg.QueryValueEx(registry_key, name)
            return value

    except WindowsError:
        return None


if __name__ == "__main__":
    reg_path = r"Control Panel\Mouse"
    print(get_reg(reg_path, "MouseSensitivity"))
    # 10
