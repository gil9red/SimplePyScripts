#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import subprocess
import sys

from is_user_admin import is_user_admin


if not is_user_admin():
    path_py_exe = sys.executable
    path_script = __file__

    args: list[str] = [
        "powershell",
        "-Command",
        f"&{{Start-Process -FilePath '{path_py_exe}' '{path_script}' -Verb RunAs}}",
    ]
    subprocess.Popen(args)

    sys.exit("This script must be run as root.")

print("You are now an administrator...")
input()
