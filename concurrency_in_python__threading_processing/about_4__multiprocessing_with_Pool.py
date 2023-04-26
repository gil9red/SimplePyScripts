#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://towardsdatascience.com/concurrency-in-python-e770c878ab53
# SOURCE: https://gist.github.com/eriky/f58b85c2d74981e6e3651d557643a0d0#file-multiproc_pooled-py


import multiprocessing
import time

from about_1__single_thread import heavy, WORKERS, N


def doit(n):
    heavy(N, n)


def pooled(n):
    # By default, our pool will have processes slots
    with multiprocessing.Pool() as pool:
        pool.map(doit, range(n))


if __name__ == "__main__":
    start = time.perf_counter()
    pooled(WORKERS)
    print(f"Elapsed {time.perf_counter() - start:.2f} secs")
    # Elapsed 4.12 secs
