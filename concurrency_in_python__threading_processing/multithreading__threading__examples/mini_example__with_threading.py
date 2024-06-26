#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import threading
import time


def run(name="main", sleep_seconds=None):
    if sleep_seconds:
        time.sleep(sleep_seconds)

    print(f'start: "{name}": {threading.current_thread()}')


if __name__ == "__main__":
    run()

    thread = threading.Thread(target=run, args=("thread #1", 3))
    thread.start()

    thread = threading.Thread(target=run, args=("thread #2", 1))
    thread.start()

    thread = threading.Thread(target=run, args=("thread #3", 0))
    thread.start()
