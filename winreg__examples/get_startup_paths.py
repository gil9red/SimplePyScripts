#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import os
import winreg

from fnmatch import fnmatch
from pathlib import Path
from typing import Tuple, List, Optional
from winreg import OpenKey, QueryValueEx, HKEYType


def get_key(path: str) -> Optional[HKEYType]:
    # Example:
    #     path = r"HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders"
    #     registry_key_name = "HKEY_LOCAL_MACHINE"
    #     relative_path = r"Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders"
    registry_key_name, relative_path = path.split('\\', maxsplit=1)
    registry_key = getattr(winreg, registry_key_name)

    try:
        return OpenKey(registry_key, relative_path)
    except:
        return


def get_registry_path(path: str, name: str) -> Path:
    key = get_key(path)
    value = QueryValueEx(key, name)[0]
    return Path(os.path.expandvars(value))


def get_common_startup_path() -> Tuple[Path, Path]:
    abs_path_startup = get_registry_path(
        r"HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders",
        'Common Startup'
    )
    return abs_path_startup, abs_path_startup / 'SystemExplorerDisabled'


def get_current_user_startup_path() -> Tuple[Path, Path]:
    abs_path_startup = get_registry_path(
        r"HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders",
        'Startup'
    )
    return abs_path_startup, abs_path_startup / 'SystemExplorerDisabled'


def get_files(path: Path, ignored_by_mask=('*.ini',)) -> List[Path]:
    items = []
    if path.exists():
        for file in path.iterdir():
            if not file.is_file() or any(fnmatch(file.name, mask) for mask in ignored_by_mask):
                continue

            items.append(file)

    return items


def get_common_startup_files() -> Tuple[List[Path], List[Path]]:
    path_startup, path_startup_disabled = get_common_startup_path()
    return get_files(path_startup), get_files(path_startup_disabled)


def get_current_user_startup_files() -> Tuple[List[Path], List[Path]]:
    path_startup, path_startup_disabled = get_current_user_startup_path()
    return get_files(path_startup), get_files(path_startup_disabled)


if __name__ == '__main__':
    assert get_key(r"HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders")
    assert get_key(r"HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders")

    abs_path_common_startup, abs_path_common_startup_disabled = get_common_startup_path()
    print(f'Exists={abs_path_common_startup.exists()} {abs_path_common_startup}')
    print(f'Exists={abs_path_common_startup_disabled.exists()} {abs_path_common_startup_disabled}')
    # Exists=True C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Startup
    # Exists=False C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Startup\SystemExplorerDisabled

    common_startup_files, common_startup_disabled_files = get_common_startup_files()
    print(
        f'common_startup_files ({len(common_startup_files)}):',
        [file.name for file in common_startup_files]
    )
    print(
        f'common_startup_disabled_files ({len(common_startup_disabled_files)}):',
        [file.name for file in common_startup_disabled_files]
    )

    print()

    abs_path_current_user_startup, abs_path_current_user_startup_disabled = get_current_user_startup_path()
    print(f'Exists={abs_path_current_user_startup.exists()} {abs_path_current_user_startup}')
    print(f'Exists={abs_path_current_user_startup_disabled.exists()} {abs_path_current_user_startup_disabled}')
    # Exists=True C:\Users\IPetrash\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup
    # Exists=False C:\Users\IPetrash\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\SystemExplorerDisabled

    current_user_startup_files, current_user_startup_disabled_files = get_current_user_startup_files()
    print(
        f'current_user_startup_files ({len(current_user_startup_files)}):',
        [file.name for file in current_user_startup_files]
    )
    print(
        f'current_user_startup_disabled_files ({len(current_user_startup_disabled_files)}):',
        [file.name for file in current_user_startup_disabled_files]
    )
