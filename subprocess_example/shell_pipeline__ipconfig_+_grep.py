#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import subprocess


command_listen = "ipconfig | grep IPv4"
process = subprocess.Popen(command_listen, stdout=subprocess.PIPE, shell=True)
print(process.communicate())
# (b'   IPv4 Address. . . . . . . . . . . : *.*.*.*\r\n', None)

sub_process = subprocess.Popen(["ipconfig"], stdout=subprocess.PIPE)
process = subprocess.Popen(
    ["grep", "IPv4"], stdin=sub_process.stdout, stdout=subprocess.PIPE
)
print(process.communicate())
# (b'   IPv4 Address. . . . . . . . . . . : *.*.*.*\r\n', None)
