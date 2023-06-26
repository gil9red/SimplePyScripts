#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import socket


request = b"GET / HTTP/1.1\nHost: stackoverflow.com\n\n"
host = "stackoverflow.com"
port = 80

sock = socket.socket()
sock.settimeout(60)  # Если за 60 секунд данные не придут, соединение закрывается
sock.connect((host, port))
sock.send(request)

SIZE = 1024

try:
    while True:
        data = sock.recv(1024)
        print(len(data), data)

        if not data or len(data) <= SIZE:
            break

except socket.timeout:
    pass
