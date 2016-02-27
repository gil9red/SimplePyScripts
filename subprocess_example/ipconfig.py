#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import subprocess

if __name__ == '__main__':
    ipconfig_res = subprocess.Popen("ipconfig", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in ipconfig_res.stdout.readlines():
        line = line.strip()
        if line:
            print(line.decode('cp866'))
