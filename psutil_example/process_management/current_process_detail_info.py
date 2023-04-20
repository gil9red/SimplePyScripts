#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from multiprocessing import current_process
from process_detail_info import print_info

pid = current_process().pid
print(pid)
print()

print_info(pid)
