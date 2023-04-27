#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import time


class TimeThis(object):
    def __init__(self, title="TimeThis"):
        self.title = title
        self.start_time = None

    def __enter__(self):
        self.start_time = time.clock()
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        print(
            f"[{self.title}] total time: {time.clock() - self.start_time:.3f} sec"
        )


if __name__ == "__main__":
    with TimeThis():
        time.sleep(1)

    with TimeThis("Test"):
        text = ""
        for i in range(10**6):
            text += str(i)

    with TimeThis("Test"):
        items = []
        for i in range(10**6):
            items.append(str(i))

        text = "".join(items)
