#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import socket
sock = socket.socket()
sock.connect(('localhost', 9090))

data = 'Hello World!'
sock.send(data.encode())

print('Close')
sock.close()
