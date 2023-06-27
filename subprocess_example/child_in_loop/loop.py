#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import sys
from subprocess import Popen, PIPE


if __name__ == "__main__":
    # with Popen('python child.py', stdin=PIPE, stdout=PIPE, shell=True) as proc:
    #     for line in proc.stdout:
    #         print(line)

    with Popen(
        [sys.executable, "-u", "child.py"], stdout=PIPE, universal_newlines=True
    ) as process:
        for line in process.stdout:
            print(line.replace("!", "#"), end="")
