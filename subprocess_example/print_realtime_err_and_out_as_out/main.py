#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


if __name__ == "__main__":
    from subprocess import Popen, PIPE, STDOUT

    with Popen(
        "python print_rand_out_and_err.py",
        shell=True,
        universal_newlines=True,
        stdout=PIPE,
        stderr=STDOUT,
    ) as process:
        print("-" * 10)
        print("Start:")

        for line in process.stdout:
            print(line, end="")

        print("End.")
        print("-" * 10)
