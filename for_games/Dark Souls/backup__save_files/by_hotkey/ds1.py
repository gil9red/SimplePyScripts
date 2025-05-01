#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# C:\Users\<CURRENT_USER>\Documents\NBGI\DarkSouls\<PLAYER_NAME>\DRAKS0005.sl2
# OR r'~\Documents\NBGI\DarkSouls\*\*.sl2'
PATH_DS_SAVE = r"~\Documents\NBGI\DarkSouls\*\DRAKS0005.sl2"


if __name__ == "__main__":
    from common import run
    # Example set another hotkey:
    # run(PATH_DS_SAVE, hotkey="Ctrl + Alt + F + D + F3")
    run(PATH_DS_SAVE)
