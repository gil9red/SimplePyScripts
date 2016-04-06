#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from subprocess import Popen, PIPE

if __name__ == '__main__':
    ipconfig_res = Popen("ipconfig", universal_newlines=True, stdout=PIPE)
    for line in ipconfig_res.stdout:
        print(line, end='')
