#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# pip install psutil
import psutil


def get_drivers() -> list[str]:
    return [x.device[0] for x in psutil.disk_partitions(all=True)]


if __name__ == "__main__":
    drives = get_drivers()
    print(drives)
