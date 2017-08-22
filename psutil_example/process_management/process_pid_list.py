#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# pip install psutil
import psutil

process_pid_list = psutil.pids()
print('Process pid list ({}): {}'.format(len(process_pid_list), process_pid_list))
