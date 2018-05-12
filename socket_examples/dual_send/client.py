#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# SOURCE: https://habrahabr.ru/post/149077/

BUFFER_SIZE = 4096


import socket
sock = socket.socket()
sock.connect(('localhost', 9090))

# Send big data
# data = ','.join(str(i) for i in range(10000))
data = 'HelloWorld!' * 10000
print('Send len: {}'.format(len(data)))
print()

sock.sendall(data.encode())

print('Response')

response_data = bytearray()

while True:
    data = sock.recv(BUFFER_SIZE)
    if not data:
        break

    print(len(data), data)
    response_data += data

print()
print('Total len: {}'.format(len(response_data)))

print('Close')
sock.close()
