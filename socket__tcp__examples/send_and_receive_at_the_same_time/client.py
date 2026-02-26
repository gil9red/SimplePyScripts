#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import socket
import sys
import time

from threading import Thread

sys.path.append("..")
from common import send_msg, recv_msg


HOST = socket.gethostname()
PORT = 9090

sock = socket.socket()
sock.connect((HOST, PORT))


def read_from() -> None:
    while True:
        response_data = recv_msg(sock)
        if response_data:
            print(f"Response ({len(response_data)}): {response_data}")
        time.sleep(0.1)


Thread(target=read_from).start()


stan = 0
while True:
    stan += 1
    if stan <= 20:
        data = f"#{stan} Hello World!".encode('utf-8')
        print(f"Sending: {data}")

        send_msg(sock, data)

    time.sleep(0.1)
