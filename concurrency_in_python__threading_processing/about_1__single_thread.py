#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://towardsdatascience.com/concurrency-in-python-e770c878ab53
# SOURCE: https://gist.github.com/eriky/0de249619e6db10fa47b7d47082b4c36#file-sequential-py


import time


WORKERS = 80
N = 500


# A CPU heavy calculation, just as an example. This can be anything you like
def heavy(n, myid) -> None:
    for x in range(1, n):
        for y in range(1, n):
            x**y
    print(myid, "is done")


def sequential(n) -> None:
    for i in range(n):
        heavy(N, i)


if __name__ == "__main__":
    start = time.perf_counter()
    sequential(WORKERS)
    print(f"Elapsed {time.perf_counter() - start:.2f} secs")
    # Elapsed 32.80 secs
