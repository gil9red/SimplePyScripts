#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


request = b"GET / HTTP/1.1\nHost: stackoverflow.com\n\n"
host = "stackoverflow.com"
port = 80

import socket
sock = socket.socket()
sock.settimeout(60)  # Если за 60 секунд данные не придут, соединение закрывается
sock.connect((host, port))
sock.send(request)

try:
    while True:
        data = sock.recv(1024)
        if not data:
            break

        print(len(data), data)

except socket.timeout:
    pass