#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import time
from datetime import datetime

from tkinter.messagebox import showinfo

from main import get_last_issue_key


NEED_PROJECT: str = "OPTT"
NEED_ISSUE_ID: int = 999


while True:
    last_issue_key: str = get_last_issue_key(NEED_PROJECT)
    print(f'{datetime.now():%d/%m/%Y %H:%M:%S} last_issue_key: {last_issue_key}')

    # NOTE: "OPTT-1234" -> 1234
    issue_id: int = int(last_issue_key.split("-")[-1])
    if issue_id >= NEED_ISSUE_ID:
        showinfo(title="Информация", message=f"Появилась задача {last_issue_key}!")

    time.sleep(30)
