#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from base64 import b64decode


def decode_base64_to_file(file_name: str, text_base64: str):
    with open(file_name, "wb") as f:
        data = b64decode(text_base64)
        f.write(data)


if __name__ == "__main__":
    # Hello World!
    text = "SGVsbG8gV29ybGQh"

    decode_base64_to_file("result.txt", text)
