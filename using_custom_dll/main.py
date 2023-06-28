#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""This example by create and build dll and using in python scripts."""


import ctypes


dll_name = "mydll2.dll"
mydll2 = ctypes.CDLL(dll_name)
print(mydll2.add(1, 2))
print(mydll2.sub(1, 2))
