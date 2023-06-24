#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import sys
import time


def f1(n):
    last_num_chars = 0

    write, flush = sys.stdout.write, sys.stdout.flush
    while n >= 0:
        write("\r" * last_num_chars)
        last_num_chars = write("[1] Left: " + str(n))
        flush()

        time.sleep(1)
        n -= 1

    print()


def f2(n):
    last_num_chars = 0

    write, flush = sys.stdout.write, sys.stdout.flush
    while n >= 0:
        write("\b" * last_num_chars)
        last_num_chars = write("[2] Left: " + str(n))
        flush()

        time.sleep(1)
        n -= 1

    print()


f1(10)
f2(10)
