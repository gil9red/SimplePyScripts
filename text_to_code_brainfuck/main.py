#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import base64
import zlib

import simple_brainfuck


def text_to_code_brainfuck(text):
    commands_brainfuck = []

    for c in text:
        commands_brainfuck.append("+" * ord(c) + ".")

    return ">".join(commands_brainfuck)


if __name__ == "__main__":
    text = "Hello World!"

    code_brainfuck = text_to_code_brainfuck(text)
    print("code_brainfuck:", len(code_brainfuck))
    # print(code_brainfuck)
    print()

    # Test generated brainfuck code
    result = simple_brainfuck.execute(code_brainfuck)
    print("result:", len(result))
    print(result)
    assert result == text

    # TODO: Compress variant
    code_brainfuck_compress = zlib.compress(code_brainfuck.encode("utf-8"))
    print()
    print("code_brainfuck_compress:", len(code_brainfuck_compress))
    print(code_brainfuck_compress)

    data = base64.b64encode(code_brainfuck_compress)
    code_brainfuck_compress_base64 = data.decode("utf-8")
    print()
    print("code_brainfuck_compress_base64:", len(code_brainfuck_compress_base64))
    print(code_brainfuck_compress_base64)

    with open("code.bf", mode="w", encoding="utf-8") as f:
        f.write(code_brainfuck)
