#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import time
from datetime import datetime

from tkinter.messagebox import showinfo

from main import get_last_issue_key


NEED_PROJECT = "OPTT"
NEED_ISSUE_KEY = f"{NEED_PROJECT}-999"


while True:
    last_issue_key = get_last_issue_key(NEED_PROJECT)
    print(f'{datetime.now():%d/%m/%Y %H:%M:%S} last_issue_key: {last_issue_key}')

    if last_issue_key == NEED_ISSUE_KEY:
        showinfo(title="Информация", message=f"Появилась задача {NEED_ISSUE_KEY}!")

    time.sleep(30)
