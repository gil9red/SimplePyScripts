#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import os.path
import zipfile

from datetime import datetime


dir_path = os.path.expanduser(r'~\Saved Games\Lionhead Studios\Fable 3\1000100010001000')

save_name = os.path.basename(dir_path)

backup_file_name = f"{save_name}_{datetime.today():%Y%m%d_%H%M%S}.backup.zip"
backup_full_file_name = os.path.join(os.path.dirname(dir_path), backup_file_name)

with zipfile.ZipFile(backup_full_file_name, mode="w") as f:
    for file in os.listdir(dir_path):
        f.write(os.path.join(dir_path, file), file)
