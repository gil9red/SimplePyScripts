#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


request = b"GET / HTTP/1.1\nHost: stackoverflow.com\n\n"
host = "stackoverflow.com"
port = 80

import socket
s = socket.socket()
s.connect((host, port))
s.send(request)

while True:
    result = s.recv(1024)
    if not result:
        break

    print(result)
