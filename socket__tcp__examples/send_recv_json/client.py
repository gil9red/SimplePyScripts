#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import json
import socket

import sys
sys.path.append("..")
from common import send_msg, recv_msg


HOST, PORT = "localhost", 9090


with socket.socket() as sock:
    sock.connect((HOST, PORT))

    data = {
        "title": "test",
        "counter": 1,
    }
    data = json.dumps(data)
    data = bytes(data, "utf-8")
    print("Sending ({}): {}".format(len(data), data))
    print()

    send_msg(sock, data)

    print("Receiving")

    response_data = recv_msg(sock)
    print("Response ({}): {}".format(len(response_data), response_data))

    print("Close\n")
