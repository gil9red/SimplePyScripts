#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://www.saule-spb.ru/library/autorun.html
# SOURCE: http://datadump.ru/virus-detection/


from common import RegistryKey


PATHS = [
    r"HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Image File Execution Options",
    r"HKLM\SOFTWARE\Wow6432Node\Microsoft\Windows NT\CurrentVersion\Image File Execution Options",
]


def get_image_file_execution_options() -> dict[str, str]:
    path_by_debuggers = dict()
    for path in PATHS:
        for sub_key in RegistryKey(path).subkeys():
            if debugger := sub_key.get_str_value("debugger"):
                path_by_debuggers[sub_key.path] = debugger

    return path_by_debuggers


if __name__ == "__main__":
    print(get_image_file_execution_options())
    # {'HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Image File Execution Options\\taskmgr.exe': '"C:\\Program Files (x86)\\System Explorer\\SystemExplorer.exe"', 'HKEY_LOCAL_MACHINE\\SOFTWARE\\Wow6432Node\\Microsoft\\Windows NT\\CurrentVersion\\Image File Execution Options\\taskmgr.exe': '"C:\\Program Files (x86)\\System Explorer\\SystemExplorer.exe"'}
