#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from pathlib import Path

from PyQt5.QtCore import QCoreApplication, QFileSystemWatcher


current_dir = str(Path(__file__).resolve().parent)


app = QCoreApplication([])

watcher = QFileSystemWatcher([current_dir])
watcher.directoryChanged.connect(lambda directory: print('Directory:', directory))
watcher.fileChanged.connect(lambda file: print('File:', file))

app.exec_()
