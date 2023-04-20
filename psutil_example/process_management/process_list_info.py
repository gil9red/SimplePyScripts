#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""Получение списка запущенных процессов."""


# pip install psutil
import psutil


for proc in psutil.process_iter():
    try:
        pinfo = proc.as_dict(attrs=["pid", "name"])
    except psutil.NoSuchProcess:
        continue

    print(pinfo)
