#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import sys
import random

from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent

sys.path.append(str(ROOT_DIR))
from add_notify import add_notify


if __name__ == '__main__':
    # Название можно передать как аргумент
    try:
        name = sys.argv[1]
    except:
        name = 'test'

    N = random.randrange(2, 5+2)
    for i in range(N):
        text = f'Rand: {i+1} / {N}'
        print(name, text)
        add_notify(name=name, message=text)
