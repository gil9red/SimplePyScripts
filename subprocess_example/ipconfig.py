#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from subprocess import Popen, PIPE


p = Popen("ipconfig", stdout=PIPE)
for line in p.stdout:
    print(line.decode('cp866'), end='')
