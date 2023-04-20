#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# pip install psutil
import psutil
from psutil._pswindows import WindowsService


def get_win_services() -> list[WindowsService]:
    return list(psutil.win_service_iter())


if __name__ == "__main__":
    win_service_list = get_win_services()
    print(f"Win service list ({len(win_service_list)}):")

    for service in win_service_list:
        title = f"{service.name()!r} ({service.display_name()})"
        path = (
            f"Pid={service.pid()}, name={service.name()!r}, display_name={service.display_name()!r}, "
            f"status={service.status()!r}, start_type={service.start_type()!r}"
        )
        print("Title:", title)
        print("Path:", path)
        print("Status:", service.status())
        print("binpath:", service.binpath())
        print()
