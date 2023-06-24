#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import pywinauto


window = pywinauto.findwindows.find_element(title_re="Microsoft Lync.*")

child = window.children()[3]
print(child.rich_text)
