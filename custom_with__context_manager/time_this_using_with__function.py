#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from contextlib import contextmanager
from timeit import default_timer


@contextmanager
def time_this(title: str = "TimeThis"):
    start_time: float = default_timer()
    try:
        yield
    finally:
        print(f"[{title}] total time: {default_timer() - start_time:.3f} sec")


if __name__ == "__main__":
    import time

    with time_this():
        time.sleep(1)

    with time_this("Test"):
        text = ""
        for i in range(10**5):
            text += str(i)

    with time_this("Test"):
        items = []
        for i in range(10**5):
            items.append(str(i))

        text = "".join(items)
