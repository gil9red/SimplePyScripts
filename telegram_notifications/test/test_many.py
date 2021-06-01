#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import sys
import subprocess
import random
import time

from multiprocessing.dummy import Pool

import test_one


def run(i):
    # Random delay 5-10 ms
    delay = random.randint(5, 10) / 1000
    time.sleep(delay)

    name = f'test #{i}'
    print('Run:', name)

    subprocess.call([sys.executable, test_one.__file__, name])


if __name__ == '__main__':
    with Pool() as p:
        p.map(run, range(1, 10 + 1))
