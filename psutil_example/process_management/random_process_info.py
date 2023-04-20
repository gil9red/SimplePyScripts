#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import random

# pip install psutil
import psutil

print("Random process info")

process_pid_list = psutil.pids()
pid = random.choice(process_pid_list)
print("Pid:", pid)

process = psutil.Process(pid)
print("Process:", process)
