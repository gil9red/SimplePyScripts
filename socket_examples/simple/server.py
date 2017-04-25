#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# SOURCE: https://habrahabr.ru/post/149077/


import socket
sock = socket.socket()
sock.bind(('', 9090))
sock.listen(1)

while True:
    conn, addr = sock.accept()
    print('connected:', addr)

    while True:
        data = conn.recv(1024)
        if not data:
            break

        conn.send(data.upper())

    conn.close()
