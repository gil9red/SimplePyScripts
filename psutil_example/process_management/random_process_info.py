#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# pip install psutil
import psutil

print('Random process info')

process_pid_list = psutil.pids()

import random
pid = random.choice(process_pid_list)
print('Pid:', pid)

process = psutil.Process(pid)
print('Process:', process)
