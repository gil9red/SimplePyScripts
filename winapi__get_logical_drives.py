#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import win32file
from win32file import (
    DRIVE_UNKNOWN,
    DRIVE_NO_ROOT_DIR,
    DRIVE_REMOVABLE,
    DRIVE_FIXED,
    DRIVE_REMOTE,
    DRIVE_CDROM,
    DRIVE_RAMDISK
)

DRIVE_TYPE_MAP = {
    # The drive type cannot be determined.
    DRIVE_UNKNOWN: 'DRIVE_UNKNOWN',

    # The root path is invalid; for example, there is no volume mounted at the specified path.
    DRIVE_NO_ROOT_DIR: 'DRIVE_NO_ROOT_DIR',

    # The drive has removable media; for example, a floppy drive, thumb drive, or flash card reader.
    DRIVE_REMOVABLE: 'DRIVE_REMOVABLE',

    # The drive has fixed media; for example, a hard disk drive or flash drive.
    DRIVE_FIXED: 'DRIVE_FIXED',

    # The drive is a remote (network) drive.
    DRIVE_REMOTE: 'DRIVE_REMOTE',

    # The drive is a CD-ROM drive.
    DRIVE_CDROM: 'DRIVE_CDROM',

    # The drive is a RAM disk.
    DRIVE_RAMDISK: 'DRIVE_RAMDISK',
}


def get_logical_drives() -> list:
    import win32file
    drivebits = win32file.GetLogicalDrives()

    drive_list = list()

    for d in range(1, 26):
        mask = 1 << d
        if drivebits & mask:
            # here if the drive is at least there
            drive_name = '%c:\\' % chr(ord('A') + d)

            drive_list.append(drive_name)

    return drive_list


if __name__ == '__main__':
    for drive_name in get_logical_drives():
        drive_type = win32file.GetDriveType(drive_name)

        print('{} : {}'.format(drive_name, DRIVE_TYPE_MAP[drive_type]))
