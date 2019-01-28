#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# SOURCE: https://stackoverflow.com/a/827397/5909792


import win32api


def get_drivers() -> list:
    drives = win32api.GetLogicalDriveStrings()
    drives = drives.split('\000')[:-1]
    return drives


if __name__ == '__main__':
    drives = get_drivers()
    print(drives)
