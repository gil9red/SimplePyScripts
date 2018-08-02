#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from multiprocessing import Process
import os


def info(title):
    print(title)
    print('module name:', __name__)
    print('parent process:', os.getppid())
    print('process id:', os.getpid())


def f(name):
    info('function f')
    print('Hello,', name)


if __name__ == '__main__':
    info('main line')
    print()

    p = Process(target=f, args=('bob',))
    p.start()
    p.join()
