#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from subprocess import Popen, PIPE

if __name__ == '__main__':
    with Popen('python child.py', stdin=PIPE, stdout=PIPE, shell=True) as proc:
        for line in proc.stdout:
            print(line)
