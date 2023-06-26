#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import pickle
import socket


BUFFER_SIZE = 4096

sock = socket.socket()
sock.bind(("", 9090))
sock.listen()

print(f"Sock name: {sock.getsockname()}")

while True:
    conn, addr = sock.accept()
    print("Connected:", addr)

    all_data = bytearray()

    while True:
        data = conn.recv(BUFFER_SIZE)
        if not data:
            break

        print(f"Recv: {len(data)}: {data}")
        all_data += data

    print(f"All data ({len(all_data)}): {all_data}")
    obj = pickle.loads(all_data)
    print("Obj:", obj)

    print("Close")
    conn.close()
