#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


"""Ловим нажатие кнопки и выходим."""


if __name__ == '__main__':
    import time
    import win32api

    while True:
        if win32api.GetAsyncKeyState(ord('Q')):
            print('press Q')
            quit()

        time.sleep(0.01)
