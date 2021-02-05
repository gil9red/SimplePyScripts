#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import pymem


pm = pymem.Pymem('python.exe')

for module in pm.list_modules():
    print(module.name)
