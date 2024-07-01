#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import socket


def is_free_port(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(("", port))
            return True
        except OSError:
            return False


if __name__ == "__main__":
    print(is_free_port(5510))
    print(is_free_port(8080))
    print(is_free_port(9999))
