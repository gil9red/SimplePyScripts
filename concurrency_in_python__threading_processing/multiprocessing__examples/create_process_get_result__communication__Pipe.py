#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from multiprocessing import Process, Pipe


def f(con, name):
    con.send("Hello, " + name)
    con.close()


if __name__ == "__main__":
    parent_conn, child_conn = Pipe()
    p = Process(target=f, args=(child_conn, "bob"))
    p.start()
    print(parent_conn.recv())  # Hello, bob
    p.join()
