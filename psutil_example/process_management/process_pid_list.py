#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# pip install psutil
import psutil

process_pid_list = psutil.pids()
print(f"Process pid list ({len(process_pid_list)}): {process_pid_list}")
