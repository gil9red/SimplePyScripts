#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# SOURCE: https://habrahabr.ru/post/149077/


import socket


HOST, PORT = "localhost", 9090
BUFFER_SIZE = 4096


with socket.socket() as sock:
    sock.connect((HOST, PORT))

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

        if len(data) < BUFFER_SIZE:
            break

    print()
    print('Total len: {}'.format(len(response_data)))

    print('Close')
