#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: http://stackoverflow.com/a/42913875/5909792
# Connect to proxy, in http request write full host address


import socket


BUFFER_SIZE = 1024

request = b"GET http://stackoverflow.com HTTP/1.1\nHost: stackoverflow.com\n\n"
host = "proxy.compassplus.ru"
port = 3128

sock = socket.socket()
sock.settimeout(60)  # Если за 60 секунд данные не придут, соединение закрывается

sock.connect((host, port))
sock.send(request)

try:
    while True:
        data = sock.recv(BUFFER_SIZE)
        if not data:
            break

        print(len(data), data)

except socket.timeout:
    pass

sock.close()
