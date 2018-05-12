#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# SOURCE: https://habrahabr.ru/post/149077/


import socket
from common import send_msg, recv_msg


HOST, PORT = "localhost", 9090


with socket.socket() as sock:
    sock.connect((HOST, PORT))

    # Send big data
    # data = ','.join(str(i) for i in range(10000))
    data = 'HelloWorld!' * 10000
    print('Sending ({}): {}'.format(len(data), data))
    print()

    send_msg(sock, data.encode())

    print('Receiving')

    response_data = recv_msg(sock)
    print('Response ({}): {}'.format(len(response_data), response_data))

    print('Close')
