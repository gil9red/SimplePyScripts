#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""Пример конвертирования кракозябры "РќРµ СѓРєР°Р·Р°РЅР° С‚РѕС‡РєР°" в человеческий вид."""


import sys

from PySide.QtGui import QApplication, QMessageBox

if __name__ == "__main__":
    app = QApplication(sys.argv)
    QMessageBox.information(None, None, open("t", encoding="utf-8").read())
