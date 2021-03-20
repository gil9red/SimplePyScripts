#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


def inf_it() -> iter:
    return iter(lambda: 0, 1)


if __name__ == '__main__':
    from tqdm import tqdm
    for _ in tqdm(inf_it()):
        pass
