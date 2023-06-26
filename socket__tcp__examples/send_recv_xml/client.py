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

    data = """\
<root>
    <title>test</title>
    <counter>1</counter>
</root>    
    """
    data = bytes(data, "utf-8")
    print(f"Sending ({len(data)}): {data}")
    print()

    send_msg(sock, data)

    print("Receiving")

    response_data = recv_msg(sock)
    print(f"Response ({len(response_data)}): {response_data}")

    print("Close\n")
