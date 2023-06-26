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

    # Send file
    with open("img.png", "rb") as f:
        data = f.read()

    print(f"Sending ({len(data)}): {data}")
    print()

    send_msg(sock, data)

    print("Receiving")

    response_data = recv_msg(sock)
    print(f"Response ({len(response_data)}): {response_data}")

    print("Close\n")
