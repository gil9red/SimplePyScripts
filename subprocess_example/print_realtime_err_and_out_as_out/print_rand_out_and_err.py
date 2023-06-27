#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


if __name__ == "__main__":
    import sys
    import random
    import time

    for i in range(10):
        file = random.choice([sys.stdout, sys.stderr])
        print(str(file.name) + " !", file=file)

        if random.randint(0, 1):
            time.sleep(2)
