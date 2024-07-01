#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import time

from pathlib import Path
from typing import Callable

# pip install filelock==3.15.4
from filelock import FileLock, Timeout


def run_with_lock(
    file_name: Path,
    on_duplicated_text: str = "Detected launch of second application. Shutting down",
    func: Callable = None,
    *func_args,
    **func_kwargs,
):
    if not func:
        raise ValueError("Argument func must be specified")

    file_name_lock = str(file_name) + ".lock"
    try:
        with FileLock(file_name_lock, timeout=0):
            func(*func_args, **func_kwargs)
    except Timeout:
        print(on_duplicated_text)


if __name__ == "__main__":
    def main():
        print("Start")
        time.sleep(20)
        print("Finish")


    file_name = Path(__file__).resolve()
    run_with_lock(file_name, func=main)
