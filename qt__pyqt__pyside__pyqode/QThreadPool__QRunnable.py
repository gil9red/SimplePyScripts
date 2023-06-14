#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import threading
import time
import random

from PyQt5.QtCore import QThreadPool, QRunnable


lock = threading.Lock()


class HelloWorldTask(QRunnable):
    def __init__(self, idx: int):
        super().__init__()

        self.idx = idx

    def run(self):
        with lock:
            print(f"[{self.idx}] Hello world from thread: {threading.current_thread()}")

        ms = random.randint(1, 10) / 1000
        time.sleep(ms)


# QThreadPool takes ownership and deletes 'hello' automatically
pool = QThreadPool.globalInstance()

for i in range(1, 100 + 1):
    hello = HelloWorldTask(idx=i)
    pool.start(hello)

pool.waitForDone()
