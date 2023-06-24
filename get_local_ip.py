#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import socket


def get_local_ip() -> str:
    return socket.gethostbyname(socket.getfqdn())


if __name__ == "__main__":
    print(get_local_ip())
