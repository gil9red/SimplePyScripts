#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://towardsdatascience.com/concurrency-in-python-e770c878ab53
# SOURCE: https://gist.github.com/eriky/0d31a21a04e069bf66831eaede7a5e59#file-multiproc-py


import multiprocessing
import time

from about_1__single_thread import heavy, WORKERS, N


def multiproc(n):
    processes = []

    for i in range(n):
        p = multiprocessing.Process(target=heavy, args=[N, i])
        processes.append(p)
        p.start()

    for p in processes:
        p.join()


if __name__ == "__main__":
    start = time.perf_counter()
    multiproc(WORKERS)
    print(f"Elapsed {time.perf_counter() - start:.2f} secs")
    # Elapsed 4.03 secs
