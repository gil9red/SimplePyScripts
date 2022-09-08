#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from winreg import OpenKey, HKEY_CURRENT_USER, HKEY_CLASSES_ROOT, QueryValueEx


def get_browser_command() -> str:
    # SOURCE: https://stackoverflow.com/a/12444963/5909792
    path = r"Software\Microsoft\Windows\CurrentVersion\Explorer\FileExts\.html\UserChoice"
    with OpenKey(HKEY_CURRENT_USER, path) as key:
        browser_id = QueryValueEx(key, 'Progid')[0]

    path = browser_id + r"\shell\open\command"
    with OpenKey(HKEY_CLASSES_ROOT, path) as key:
        command = QueryValueEx(key, '')[0]

    return command


if __name__ == '__main__':
    print(get_browser_command())
    # "C:\Program Files\Mozilla Firefox\firefox.exe" -osint -url "%1"
