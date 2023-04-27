#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import os
import time
from glob import glob
import traceback

# For import utils.py
import sys
sys.path.append("..")

from utils import get_logger, backup


log = get_logger(__file__)


def backup_saves(path_ds_save: str, forced=False):
    try:
        for path_file_name in glob(path_ds_save):
            log.debug(f"Check: {path_file_name}")

            # Get timestamps
            save_timestamp = os.path.getmtime(path_file_name)
            now_timestamp = time.time()

            # Save backup. If less than 600 secs have passed since the last modification of the file
            is_modified = (now_timestamp - save_timestamp) < 600
            ok = forced or is_modified
            log.debug(
                f"{'Need backup' if ok else 'Not need backup'}. "
                f"Reason: Forced={forced}, Is modified file save={is_modified}"
            )
            if not ok:
                continue

            file_name_backup = backup(path_file_name, now_timestamp)
            log.debug(f"Saving backup: {file_name_backup}")

    except:
        print("ERROR:\n" + traceback.format_exc())
        time.sleep(5 * 60)


def run(path_ds_save: str, timeout_minutes=5):
    # Example: r'~\Documents\NBGI\DarkSouls\*\DRAKS0005.sl2'
    path_ds_save = os.path.expanduser(path_ds_save)

    print(f"{path_ds_save}\n")

    backup_saves(path_ds_save, forced=True)

    while True:
        print(f"\nSleeping for {timeout_minutes} minutes\n")
        time.sleep(timeout_minutes * 60)

        backup_saves(path_ds_save, False)
