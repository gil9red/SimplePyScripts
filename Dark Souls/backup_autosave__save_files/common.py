#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from glob import glob
import os
import time
import shutil


def get_logger(name):
    import logging
    log = logging.getLogger(name)
    log.setLevel(logging.DEBUG)

    formatter = logging.Formatter('[%(asctime)s] %(message)s')

    import sys
    sh = logging.StreamHandler(stream=sys.stdout)
    sh.setFormatter(formatter)
    log.addHandler(sh)

    return log


log = get_logger(__file__)


def backup_saves(path_ds_save, forced=False):
    for path_file_name in glob(path_ds_save):
        log.debug(f"Check: {path_file_name}")

        path_dir, file_name = os.path.split(path_file_name)

        # Get timestamps
        save_timestamp = os.path.getmtime(path_file_name)
        now_timestamp = time.time()

        # Save backup. If less than 600 secs have passed since the last modification of the file
        is_modified = (now_timestamp - save_timestamp) < 600
        ok = forced or is_modified
        log.debug(f"{'Need backup' if ok else 'Not need backup'}. "
                  f"Reason: Forced={forced}, Is modified file save={is_modified}")
        if not ok:
            continue

        path_dir_backup = os.path.join(path_dir, "BACKUP")

        # Create backup dir
        os.makedirs(path_dir_backup, exist_ok=True)

        time_backup = time.strftime("%y-%m-%d_%H%M%S", time.localtime(now_timestamp))
        file_name_backup = file_name + '.backup_' + time_backup
        file_name_backup = os.path.join(path_dir_backup, file_name_backup)

        shutil.copyfile(path_file_name, file_name_backup)

        log.debug(f"Saving backup: {file_name_backup}")
        print()


def run(path_ds_save, timeout_minutes=5):
    # Example: r'~\Documents\NBGI\DarkSouls\*\DRAKS0005.sl2'
    path_ds_save = os.path.expanduser(path_ds_save)

    backup_saves(path_ds_save, forced=True)

    while True:
        print(f"Sleeping for {timeout_minutes} minutes\n")
        time.sleep(timeout_minutes * 60)

        backup_saves(path_ds_save, False)
