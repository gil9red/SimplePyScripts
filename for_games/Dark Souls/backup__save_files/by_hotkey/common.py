#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import os
import time
import traceback
import winsound

from glob import glob

# For import utils.py
import sys
sys.path.append("..")

from utils import get_logger, backup

# pip install keyboard
import keyboard


def beep():
    try:
        winsound.Beep(1000, duration=50)
    except:
        # ignore
        pass


log = get_logger(__file__)

# Default hotkey
HOTKEY = "CTRL + F1"


def backup_saves(path_ds_save: str):
    try:
        for path_file_name in glob(path_ds_save):
            file_name_backup = backup(path_file_name)
            log.debug(f"Saving backup: {file_name_backup}")

        beep()

    except:
        print("ERROR:\n" + traceback.format_exc())
        time.sleep(5 * 60)


def run(path_ds_save: str, hotkey: str = HOTKEY):
    # Example: r'~\Documents\NBGI\DarkSouls\*\DRAKS0005.sl2'
    path_ds_save = os.path.expanduser(path_ds_save)

    print(f"{path_ds_save}")
    print(f"Using hotkey: {hotkey}\n")

    # Run hotkey
    keyboard.add_hotkey(hotkey, lambda: backup_saves(path_ds_save))
    keyboard.wait()
