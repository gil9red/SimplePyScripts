#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# SOURCE: https://stackoverflow.com/a/17668009/5909792


import struct


def send_msg(sock, msg):
    # Prefix each message with a 4-byte length (network byte order)
    msg = struct.pack('>I', len(msg)) + msg
    sock.sendall(msg)


def recv_msg(sock):
    # Read message length and unpack it into an integer
    raw_msglen = recv_all(sock, 4)
    if not raw_msglen:
        return None

    msg_len = struct.unpack('>I', raw_msglen)[0]

    # Read the message data
    return recv_all(sock, msg_len)


def recv_all(sock, n):
    # Helper function to recv n bytes or return None if EOF is hit
    data = bytearray()

    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None

        data += packet

    return bytes(data)
