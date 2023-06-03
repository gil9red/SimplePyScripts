#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# pip install pymem
from pymem import Pymem


pm = Pymem("notepad.exe")
print("Process id: %s" % pm.process_id)
address = pm.allocate(10)
print("Allocated address: %s" % address)
pm.write_int(address, 1337)
value = pm.read_int(address)
print("Allocated value: %s" % value)
pm.free(address)
