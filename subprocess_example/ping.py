#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from subprocess import Popen, PIPE

if __name__ == '__main__':
    ipconfig_res = Popen("ping ya.ru", universal_newlines=True, stdout=PIPE)
    for line in ipconfig_res.stdout:
        print(line, end='')


# import subprocess
#
# if __name__ == '__main__':
#     ping_res = subprocess.Popen("ping ya.ru", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
#     for line in ping_res.stdout.readlines():
#         line = line.rstrip()
#         if line:
#             print(line.decode('cp866'))
