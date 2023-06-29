#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import datetime as dt
from pathlib import Path

from PyQt5.QtCore import QCoreApplication, QFileSystemWatcher


current_dir = str(Path(__file__).resolve().parent)

app = QCoreApplication([])

watcher = QFileSystemWatcher([current_dir])
watcher.directoryChanged.connect(
    lambda directory: print(
        f"[{dt.datetime.now():%d/%m/%Y %H:%M:%S}] Directory: {directory!r}"
    )
)
watcher.fileChanged.connect(
    lambda file: print(f"[{dt.datetime.now():%d/%m/%Y %H:%M:%S}] File: {file!r}")
)

app.exec_()
