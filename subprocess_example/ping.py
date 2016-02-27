#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import subprocess

if __name__ == '__main__':
    ping_res = subprocess.Popen("ping ya.ru", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in ping_res.stdout.readlines():
        line = line.rstrip()
        if line:
            print(line.decode('cp866'))
