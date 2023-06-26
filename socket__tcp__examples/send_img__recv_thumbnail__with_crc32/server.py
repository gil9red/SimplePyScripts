#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import io
import socket

from PIL import Image

import sys
sys.path.append("..")
from common import send_msg__with_crc32, recv_msg__with_crc32


PORT = 9090


with socket.socket() as sock:
    sock.bind(("", PORT))
    sock.listen()

    print(f"Server: {sock.getsockname()}")

    while True:
        conn, addr = sock.accept()
        print("Connected:", addr)

        data = recv_msg__with_crc32(conn)
        print(f"Receiving {len(data)} bytes")

        img = Image.open(io.BytesIO(data))
        print("Receiving image:", img)

        print("Transform image in thumbnail")

        # Transform in thumbnail
        img.thumbnail((75, 75))

        print("Img:", img)

        # Write thumbnail in buffer
        data_io = io.BytesIO()
        img.save(data_io, "jpeg")

        response_data = data_io.getvalue()

        print(f"Sending {len(response_data)} bytes")

        send_msg__with_crc32(conn, response_data)

        print("Close\n")
