#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


if __name__ == '__main__':
    import sys

    if len(sys.argv) > 1:
        text = ' '.join(sys.argv[1:])
        print('Text: "{}"'.format(text))

        from PySide.QtGui import QApplication
        app = QApplication(sys.argv)
        app.clipboard().setText(text)
    else:
        import os
        file_name = os.path.basename(sys.argv[0])
        print('usage: {} [-h] text'.format(file_name))
