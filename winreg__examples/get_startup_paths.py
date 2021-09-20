#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import os

from pathlib import Path
from typing import Tuple
from winreg import HKEY_CURRENT_USER, HKEY_LOCAL_MACHINE, OpenKey, QueryValueEx


def get_registry_path(registry_key: int, key: str, name: str) -> Path:
    key = OpenKey(registry_key, key)
    value = QueryValueEx(key, name)[0]
    return Path(os.path.expandvars(value))


def get_common_startup_path() -> Tuple[Path, Path]:
    abs_path_startup = get_registry_path(
        HKEY_LOCAL_MACHINE,
        r"Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders",
        'Common Startup'
    )
    return abs_path_startup, abs_path_startup / 'SystemExplorerDisabled'


def get_current_user_startup_path() -> Tuple[Path, Path]:
    abs_path_startup = get_registry_path(
        HKEY_CURRENT_USER,
        r"Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders",
        'Startup'
    )
    return abs_path_startup, abs_path_startup / 'SystemExplorerDisabled'


if __name__ == '__main__':
    abs_path_startup, abs_path_startup_disabled = get_common_startup_path()
    print(abs_path_startup.exists(), abs_path_startup)
    print(abs_path_startup_disabled.exists(), abs_path_startup_disabled)
    # True C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Startup
    # False C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Startup\SystemExplorerDisabled

    print()

    abs_path_startup, abs_path_startup_disabled = get_current_user_startup_path()
    print(abs_path_startup.exists(), abs_path_startup)
    print(abs_path_startup_disabled.exists(), abs_path_startup_disabled)
    # True C:\Users\IPetrash\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup
    # True C:\Users\IPetrash\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\SystemExplorerDisabled
