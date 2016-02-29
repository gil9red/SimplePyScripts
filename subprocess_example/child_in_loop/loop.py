#!/usr/bin/env python3

__author__ = 'ipetrash'


from subprocess import Popen, PIPE

if __name__ == '__main__':
    with Popen('python child.py', stdout=PIPE, universal_newlines=True) as proc:
        for line in proc.stdout:
            print(line, end='')
