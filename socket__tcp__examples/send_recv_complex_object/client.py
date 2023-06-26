#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import pickle
import socket


sock = socket.socket()
sock.connect(("localhost", 9090))

obj = {
    "a": 1,
    "b": [2, 3],
    "c": {
        "c1": "abc",
    },
}

print("Send:", obj)

data = pickle.dumps(obj)
sock.sendall(data)

print("Close")
sock.close()
