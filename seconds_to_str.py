#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


def seconds_to_str(seconds: int | float) -> str:
    hh, mm = divmod(seconds, 3600)
    mm, ss = divmod(mm, 60)
    return "%02d:%02d:%02d" % (hh, mm, ss)


if __name__ == "__main__":
    print(seconds_to_str(1))  # 00:00:01
    assert seconds_to_str(1) == "00:00:01"

    print(seconds_to_str(60))  # 00:01:00
    assert seconds_to_str(60) == "00:01:00"

    print(seconds_to_str(3600))  # 01:00:00
    assert seconds_to_str(3600) == "01:00:00"

    print(seconds_to_str(3678))  # 01:01:18
    assert seconds_to_str(3678) == "01:01:18"

    print(seconds_to_str(8888))  # 02:28:08
    assert seconds_to_str(8888) == "02:28:08"

    print(seconds_to_str(27355))  # 07:35:55
    assert seconds_to_str(27355) == "07:35:55"

    print(seconds_to_str(27355.0))  # 07:35:55
    assert seconds_to_str(27355.0) == "07:35:55"
