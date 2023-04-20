#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import json
import pathlib
from typing import List, Union

# pip install psutil
import psutil


# Absolute file name
FILE_NAME_SNAPSHOT = str(pathlib.Path(__file__).resolve().parent / "snapshot.json")


def sizeof_fmt(num: Union[int, float], with_sign=False) -> str:
    if with_sign:
        sign = "+" if num >= 0 else "-"
    else:
        sign = ""

    if num == 0:
        sign = ""

    num = abs(num)

    for x in ["bytes", "KB", "MB", "GB"]:
        if num < 1024.0:
            return "%s%3.1f %s" % (sign, num, x)

        num /= 1024.0

    return "%s%3.1f %s" % (sign, num, "TB")


def get_disc_list() -> List[str]:
    return [disk.device for disk in psutil.disk_partitions() if "fixed" in disk.opts]


def get_human_sizes(items: List[int], with_sign) -> List[str]:
    return [sizeof_fmt(x, with_sign) for x in items]


def get_disc_used(disc_list: List[str] = None, only_raw=False) -> List[Union[int, str]]:
    if disc_list is None:
        disc_list = get_disc_list()

    if only_raw:
        return [psutil.disk_usage(disk).used for disk in disc_list]

    return [sizeof_fmt(psutil.disk_usage(disk).used) for disk in disc_list]


def get_disc_total_used(disc_list: List[str]) -> str:
    return sizeof_fmt(sum(psutil.disk_usage(disk).used for disk in disc_list))


def write_snapshot_raw_disc_used(disc_list: List[str] = None):
    with open(FILE_NAME_SNAPSHOT, "w", encoding="utf-8") as f:
        items = get_disc_used(disc_list, only_raw=True)
        print("Write snapshot with:", items)

        json.dump(items, f)


def load_snapshot_raw_disc_used() -> List[int]:
    with open(FILE_NAME_SNAPSHOT, encoding="utf-8") as f:
        items = json.load(f)
        print("Read snapshot:", items)

        return items


def get_row_for(name: str, disc_list_raw: List[int], with_sign=False) -> List[str]:
    row = [name]
    row.extend(get_human_sizes(disc_list_raw, with_sign))
    row.append(sizeof_fmt(sum(disc_list_raw), with_sign))
    return row
