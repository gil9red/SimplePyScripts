#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://stackoverflow.com/a/19719292/5909792


import ctypes
import os
import traceback


def is_windows() -> bool:
    return os.name == "nt"


# Linux or mac
def is_posix() -> bool:
    return os.name == "posix"


def is_user_admin() -> bool:
    if is_windows():
        try:
            # WARNING: Requires Windows XP SP2 or higher!
            return bool(ctypes.windll.shell32.IsUserAnAdmin())

        except:
            traceback.print_exc()
            print("Admin check failed, assuming not an admin.")
            return False

    elif is_posix():
        # Check for root on Posix
        return os.geteuid() == 0

    else:
        raise RuntimeError(f"Unsupported operating system for this module: {os.name}")


if __name__ == "__main__":
    print("is_user_admin:", is_user_admin())
