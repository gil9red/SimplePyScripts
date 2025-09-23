#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from timeit import default_timer


class TimeThis:
    def __init__(self, title: str = "TimeThis"):
        self.title: str = title
        self.start_time: float = 0.0

    def __enter__(self) -> "TimeThis":
        self.start_time = default_timer()
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        print(f"[{self.title}] total time: {default_timer() - self.start_time:.3f} sec")


if __name__ == "__main__":
    import time

    with TimeThis():
        time.sleep(1)

    with TimeThis("Test"):
        text = ""
        for i in range(10**5):
            text += str(i)

    with TimeThis("Test"):
        items = []
        for i in range(10**5):
            items.append(str(i))

        text = "".join(items)
