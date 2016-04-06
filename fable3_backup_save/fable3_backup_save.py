#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# Backups


if __name__ == '__main__':
    dir_path = r'C:\Users\ipetrash\Saved Games\Lionhead Studios\Fable 3\1000100010001000'

    from datetime import datetime as dt
    import os

    save_name = os.path.basename(dir_path)

    backup_file_name = '{}_{}.backup.zip'.format(save_name, dt.today().strftime('%Y%m%d_%H%M%S'))
    backup_full_file_name = os.path.join(os.path.dirname(dir_path), backup_file_name)

    import zipfile

    with zipfile.ZipFile(backup_full_file_name, mode="w") as f:
        for file in os.listdir(dir_path):
            f.write(os.path.join(dir_path, file), file)
