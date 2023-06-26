#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import socket

import sys
sys.path.append("..")
from common import send_msg, recv_msg


HOST, PORT = "localhost", 9090


with socket.socket() as sock:
    sock.connect((HOST, PORT))

    # Send big data
    # data = ','.join(str(i) for i in range(10000))
    data = "HelloWorld!" * 10000
    print(f"Sending ({len(data)}): {data}")
    data = data.encode()
    print()

    send_msg(sock, data)

    print("Receiving")

    response_data = recv_msg(sock)
    print(f"Response ({len(response_data)}): {response_data}")

    print("Close\n")
