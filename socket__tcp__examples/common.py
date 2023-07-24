#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://stackoverflow.com/a/17668009/5909792


import struct
import zlib


def crc32_from_bytes(data: bytes) -> int:
    return zlib.crc32(data) & 0xFFFFFFFF


def send_msg__with_crc32(sock, msg):
    # Prefix each message with a 12-byte (network byte order) length: 8-byte data length and 4-byte crc32 data
    crc32 = crc32_from_bytes(msg)
    msg = struct.pack(">QI", len(msg), crc32) + msg

    sock.sendall(msg)


def recv_msg__with_crc32(sock) -> bytes | None:
    # 12-byte
    payload_size = struct.calcsize(">QI")

    # Read message length and crc32
    raw_msg_len = recv_all(sock, payload_size)
    if not raw_msg_len:
        return None

    msg_len, crc32 = struct.unpack(">QI", raw_msg_len)

    # Read the message data
    msg = recv_all(sock, msg_len)

    # Check message
    msg_crc32 = crc32_from_bytes(msg)
    if msg_crc32 != crc32:
        raise Exception(
            f"Incorrect message: invalid crc32. Receiving crc32: {crc32}, current: {msg_crc32}"
        )

    return msg


def send_msg(sock, msg, msg_len_format: str = ">Q"):
    # Prefix each message with a 8-byte (>Q) length (network byte order)
    msg = struct.pack(msg_len_format, len(msg)) + msg
    sock.sendall(msg)


def recv_msg(sock, msg_len_format: str = ">Q") -> bytes | None:
    # >Q - 8-byte
    payload_size = struct.calcsize(msg_len_format)

    # Read message length and unpack it into an integer
    raw_msg_len = recv_all(sock, payload_size)
    if not raw_msg_len:
        return None

    msg_len = struct.unpack(msg_len_format, raw_msg_len)[0]

    # Read the message data
    return recv_all(sock, msg_len)


def recv_all(sock, n) -> bytes | None:
    # Helper function to recv n bytes or return None if EOF is hit
    data = bytearray()

    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None

        data += packet

    return bytes(data)
