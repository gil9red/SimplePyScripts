#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# pip install psutil
import psutil


print("System memory:", psutil.virtual_memory())
print("System swap memory:", psutil.swap_memory())
