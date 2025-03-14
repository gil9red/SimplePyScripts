#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://stackoverflow.com/a/33117579/5909792


import socket


def internet(host: str = "8.8.8.8", port: int = 53, timeout: float = 3):
    """
    Host: 8.8.8.8 (google-public-dns-a.google.com)
    OpenPort: 53/tcp
    Service: domain (DNS/TCP)
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        s.connect((host, port))
        return True
    except socket.error as e:
        print(f"Error: {e}")
        return False


if __name__ == "__main__":
    print(internet())
