#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# SOURCE: https://habrahabr.ru/post/149077/

BUFFER_SIZE = 1024


import socket
sock = socket.socket()
sock.connect(('localhost', 9090))

# Send big data
data = ','.join(str(i) for i in range(1000))
sock.send(data.encode())

print('Response')

while True:
    data = sock.recv(1024)
    if not data:
        break

    print(len(data), data)
    if len(data) < BUFFER_SIZE:
        break

print('Close')
sock.close()
