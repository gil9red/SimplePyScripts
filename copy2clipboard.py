#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


try:
    from PyQt5.QtGui import QGuiApplication as QApplication

except ImportError:
    try:
        from PyQt4.QtGui import QApplication

    except ImportError:
        from PySide.QtGui import QApplication


def to(text: str):
    app = QApplication([])
    app.clipboard().setText(text)
    app = None


if __name__ == "__main__":
    import sys
    import os

    if len(sys.argv) > 1:
        text = " ".join(sys.argv[1:])
        print(f'Text: "{text}"')
        to(text)
    else:
        file_name = os.path.basename(sys.argv[0])
        print(f"usage: {file_name} [-h] text")
