#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from multiprocessing import Process, Queue


def f(q, name) -> None:
    q.put("Hello, " + name)


if __name__ == "__main__":
    q = Queue()
    p = Process(target=f, args=(q, "bob"))
    p.start()
    print(q.get())  # Hello, bob
    p.join()
