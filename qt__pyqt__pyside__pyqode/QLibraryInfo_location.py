#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from PyQt5.QtCore import QLibraryInfo


print(QLibraryInfo.location(QLibraryInfo.TranslationsPath))
print(QLibraryInfo.location(QLibraryInfo.PluginsPath))
print(QLibraryInfo.location(QLibraryInfo.ExamplesPath))
"""
C:/Users/ipetrash/AppData/Local/Programs/Python/Python310/lib/site-packages/PyQt5/Qt5/translations
C:/Users/ipetrash/AppData/Local/Programs/Python/Python310/lib/site-packages/PyQt5/Qt5/plugins
C:/Users/ipetrash/AppData/Local/Programs/Python/Python310/lib/site-packages/PyQt5/Qt5/examples
"""
