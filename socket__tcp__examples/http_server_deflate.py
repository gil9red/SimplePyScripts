#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import socket
import zlib


PORT = 8080


def send_answer(conn, status="200 OK", typ="text/plain; charset=utf-8", data=b"") -> None:
    conn.send(b"GET HTTP/1.1 " + status.encode("utf-8") + b"\r\n")
    conn.send(b"Server: simplehttp\r\n")
    conn.send(b"Connection: close\r\n")
    conn.send(b"Content-Type: " + typ.encode("utf-8") + b"\r\n")
    conn.send(b"Content-Encoding: deflate\r\n")
    conn.send(b"Content-Length: " + str(len(data)).encode() + b"\r\n")
    conn.send(b"\r\n")  # После пустой строки в HTTP начинаются данные
    conn.send(data)


with socket.socket() as sock:
    sock.bind(("", PORT))
    sock.listen()

    print(f"Server: {sock.getsockname()}")

    while True:
        conn, addr = sock.accept()
        print("Connected:", addr)

        while True:
            data = conn.recv(8096)
            if not data:
                break

            print(f"Receiving ({len(data)}): {data}")
            header, body = data.split(b"\r\n\r\n")

            compress_len = len(body)
            body = zlib.decompress(body)

            rs = f"{compress_len} -> {len(body)} bytes"
            print(f"Sending ({len(rs)}): {rs}")

            rs = rs.encode("utf-8")
            rs = zlib.compress(rs)
            send_answer(conn, data=rs)

        print("Close\n")
