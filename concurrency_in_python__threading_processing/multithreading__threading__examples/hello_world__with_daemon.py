#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import threading
import time


def run() -> None:
    print(threading.current_thread())
    for i in "Hello World!":
        print(i)
        time.sleep(0.2)


if __name__ == "__main__":
    thread = threading.Thread(target=run, daemon=True)
    thread.start()

    # Main process NOT WAIT thread
