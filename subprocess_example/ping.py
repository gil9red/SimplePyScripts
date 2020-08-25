#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from subprocess import Popen, PIPE, STDOUT


ping_res = Popen("ping ya.ru", stdout=PIPE, stderr=STDOUT)

text = ''
for line in ping_res.stdout.readlines():
    line = line.decode('cp866')
    text += line

print(text)
