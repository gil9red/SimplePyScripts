#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://towardsdatascience.com/concurrency-in-python-e770c878ab53
# SOURCE: https://gist.github.com/eriky/613d2595aeab93d587c5fe6e1171d394#file-threads-py


import threading
import time

from about_1__single_thread import heavy, WORKERS, N


def threaded(n):
    threads = []

    for i in range(n):
        t = threading.Thread(target=heavy, args=[N, i])
        threads.append(t)
        t.start()

    for t in threads:
        t.join()


if __name__ == "__main__":
    start = time.perf_counter()
    threaded(WORKERS)
    print(f"Elapsed {time.perf_counter() - start:.2f} secs")
    # Elapsed 33.80 secs

    # If the heavy function had a lot of blocking IO, like network calls or
    # filesystem operations, this would be a big optimization though

    # The reason this is *not* an optimization for CPU bound functions, is the GIL!
