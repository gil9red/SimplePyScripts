#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# SOURCE: http://stackoverflow.com/a/42913875/5909792
# Connect to proxy, in http request write full host address

request = b"GET http://stackoverflow.com HTTP/1.1\nHost: stackoverflow.com\n\n"
host = "<proxy_host>"
port = 3128

import socket
s = socket.socket()
s.connect((host, port))
s.send(request)

while True:
    result = s.recv(1024)
    if not result:
        break

    print(result)
