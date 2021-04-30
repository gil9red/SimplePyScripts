#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from PyQt5.QtWidgets import QApplication


app = QApplication([])

screens = app.screens()
print(f'Screens ({len(screens)}):')

for screen in screens:
    print(f'    {screen.availableGeometry()} {screen.availableSize()}')

