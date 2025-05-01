#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import logging
import os
import time
import shutil
import sys


def get_logger(name: str):
    log = logging.getLogger(name)
    log.setLevel(logging.DEBUG)

    formatter = logging.Formatter("[%(asctime)s] %(message)s")

    sh = logging.StreamHandler(stream=sys.stdout)
    sh.setFormatter(formatter)
    log.addHandler(sh)

    return log


def backup(path_file_name: str, now_timestamp: float | None = None) -> str:
    if now_timestamp is None:
        now_timestamp = time.time()

    path_dir, file_name = os.path.split(path_file_name)

    path_dir_backup = os.path.join(path_dir, "BACKUP")

    # Create backup dir
    os.makedirs(path_dir_backup, exist_ok=True)

    time_backup = time.strftime("%y-%m-%d_%H%M%S", time.localtime(now_timestamp))
    file_name_backup = f"{file_name}.backup_{time_backup}"
    file_name_backup = os.path.join(path_dir_backup, file_name_backup)

    shutil.copyfile(path_file_name, file_name_backup)

    return file_name_backup
