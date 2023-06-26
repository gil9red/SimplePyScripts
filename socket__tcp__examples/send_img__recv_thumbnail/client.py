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
    with open("img.jpg", "rb") as f:
        data = f.read()

    print(f"Sending {len(data)} bytes")
    print()

    send_msg(sock, data)

    print("Receiving")

    response_data = recv_msg(sock)
    print(f"Response {len(response_data)} bytes")

    file_name = "img_thumbnail.jpg"
    print("Save in " + file_name)

    with open(file_name, "wb") as f:
        f.write(response_data)

    print("Close\n")
