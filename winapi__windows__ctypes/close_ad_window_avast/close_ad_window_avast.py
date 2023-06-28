#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""Script to detect and close Avast advertising windows."""


import logging
import sys

import win32gui
import win32con


def get_logger():
    log = logging.getLogger(__name__)
    log.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        "[%(asctime)s] %(filename)s[LINE:%(lineno)d] %(levelname)-8s %(message)s"
    )

    fh = logging.FileHandler("log", encoding="utf-8")
    fh.setLevel(logging.DEBUG)

    ch = logging.StreamHandler(stream=sys.stdout)
    ch.setLevel(logging.DEBUG)

    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    log.addHandler(fh)
    log.addHandler(ch)

    return log


log = get_logger()


# TODO: не все окна являются рекламными, это может быть окно сканирования системы
def close_ad():
    hwnd = win32gui.FindWindow("asw_av_popup_wndclass", None)
    if hwnd:
        log.debug("Found Avast advertising window, close it.")

        # Send close window command
        win32gui.SendMessage(hwnd, win32con.WM_CLOSE, 0, 0)


if __name__ == "__main__":
    import time

    try:
        log.debug("Start")

        while True:
            close_ad()
            time.sleep(0.2)

    finally:
        log.debug("Finish")
