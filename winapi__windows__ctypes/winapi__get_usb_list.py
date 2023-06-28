#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import win32file
from winapi__get_logical_drives import get_logical_drives


def locate_usb() -> list:
    usb_list = list()

    for drive_name in get_logical_drives():
        drive_type = win32file.GetDriveType(drive_name)

        if drive_type == win32file.DRIVE_REMOVABLE:
            usb_list.append(drive_name)

    return usb_list


if __name__ == "__main__":
    print(locate_usb())
