#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import random


class UserAgent:
    @classmethod
    def get_win_version(cls) -> float:
        return 10.0

    @classmethod
    def get_chrome_version(cls) -> str:
        a = random.randint(40, 69)
        b = random.randint(2987, 3497)
        c = random.randint(80, 140)
        return '{}.0.{}.{}'.format(a, b, c)

    @classmethod
    def get(cls) -> str:
        a = 'Mozilla/5.0 (Windows NT {}; Win64; x64)'.format(cls.get_win_version())
        b = 'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{} Safari/537.36'.format(cls.get_chrome_version())
        return '{} {}'.format(a, b)


if __name__ == '__main__':
    print(UserAgent.get())
    # Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36
    # (KHTML, like Gecko) Chrome/41.0.2993.140 Safari/537.36
