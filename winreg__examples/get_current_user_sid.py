#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from pathlib import Path
from common import RegistryKey


PATH = r"HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\ProfileList"
DIR_CURRENT_USER = str(Path("~").expanduser())


def get_current_user_sid() -> str:
    for key_sid in RegistryKey(PATH).subkeys():
        profile_image_path = key_sid.get_str_value("ProfileImagePath")
        if profile_image_path == DIR_CURRENT_USER:
            return key_sid.name

    raise Exception(f"Current user SID for {DIR_CURRENT_USER} not found!")


if __name__ == "__main__":
    print(get_current_user_sid())
