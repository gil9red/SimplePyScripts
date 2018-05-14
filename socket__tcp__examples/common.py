#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# SOURCE: https://stackoverflow.com/a/17668009/5909792


import struct
import zlib


def crc32_from_bytes(data: bytes) -> int:
    return zlib.crc32(data) & 0xFFFFFFFF


def send_msg__with_crc32(sock, msg):
    # Prefix each message with a 12-byte (network byte order) length: 8-byte data length and 4-byte crc32 data
    crc32 = crc32_from_bytes(msg)
    msg = struct.pack('>QI', len(msg), crc32) + msg

    sock.sendall(msg)


def recv_msg__with_crc32(sock):
    # Read message length and crc32
    raw_msg_len = recv_all(sock, 12)
    if not raw_msg_len:
        return None

    msg_len, crc32 = struct.unpack('>QI', raw_msg_len)

    # Read the message data
    msg = recv_all(sock, msg_len)

    # Check message
    msg_crc32 = crc32_from_bytes(msg)
    if msg_crc32 != crc32:
        raise Exception('Incorrect message: invalid crc32. Receiving crc32: {}, current: {}'.format(crc32, msg_crc32))

    return msg


def send_msg(sock, msg):
    # Prefix each message with a 8-byte length (network byte order)
    msg = struct.pack('>Q', len(msg)) + msg
    sock.sendall(msg)


def recv_msg(sock):
    # Read message length and unpack it into an integer
    raw_msg_len = recv_all(sock, 8)
    if not raw_msg_len:
        return None

    msg_len = struct.unpack('>Q', raw_msg_len)[0]

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
