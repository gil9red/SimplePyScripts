#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


try:
    from PyQt4.QtCore import QSettings
except:
    from PyQt5.QtCore import QSettings


if __name__ == "__main__":
    config = QSettings("config.ini", QSettings.IniFormat)

    counter = int(config.value("counter", 0))
    config.setValue("counter", counter + 1)

    config.setValue("key2", "abc")
