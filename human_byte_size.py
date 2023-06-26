#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


def sizeof_fmt(num: int | float) -> str:
    for x in ["bytes", "KB", "MB", "GB"]:
        if num < 1024.0:
            return "%.1f %s" % (num, x)

        num /= 1024.0

    return "%.1f %s" % (num, "TB")


if __name__ == "__main__":
    print(sizeof_fmt(25000000000))
    print()

    import shutil

    usage = shutil.disk_usage("C://")
    print(f"total: {sizeof_fmt(usage.total):>8} ({usage.total} bytes)")
    print(f"used:  {sizeof_fmt(usage.used):>8} ({usage.used} bytes)")
    print(f"free:  {sizeof_fmt(usage.free):>8} ({usage.free} bytes)")
