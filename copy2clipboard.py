#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import sys


def to(text):
    try:
        from PyQt4.QtGui import QApplication
    except ImportError:
        from PySide.QtGui import QApplication

    app = QApplication(sys.argv)
    app.clipboard().setText(text)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        text = ' '.join(sys.argv[1:])
        print('Text: "{}"'.format(text))
        to(text)

    else:
        import os
        file_name = os.path.basename(sys.argv[0])
        print('usage: {} [-h] text'.format(file_name))
