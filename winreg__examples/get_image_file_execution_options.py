#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# SOURCE: https://www.saule-spb.ru/library/autorun.html
# SOURCE: http://datadump.ru/virus-detection/


from typing import Dict
from common import get_entry, get_subkeys


PATHS = [
    r"HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Image File Execution Options",
    r"HKLM\SOFTWARE\Wow6432Node\Microsoft\Windows NT\CurrentVersion\Image File Execution Options",
]


def get_image_file_execution_options() -> Dict[str, str]:
    path_by_debuggers = dict()
    for path in PATHS:
        for sub_key_name, sub_key in get_subkeys(path):
            path_exe = fr'{path}\{sub_key_name}'
            debugger = get_entry(path_exe, 'debugger')
            if debugger and debugger.value:
                path_by_debuggers[path_exe] = debugger.value

    return path_by_debuggers


if __name__ == '__main__':
    print(get_image_file_execution_options())
    # {'HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Image File Execution Options\\taskmgr.exe': '"C:\\Program Files (x86)\\System Explorer\\SystemExplorer.exe"', 'HKLM\\SOFTWARE\\Wow6432Node\\Microsoft\\Windows NT\\CurrentVersion\\Image File Execution Options\\taskmgr.exe': '"C:\\Program Files (x86)\\System Explorer\\SystemExplorer.exe"'}
