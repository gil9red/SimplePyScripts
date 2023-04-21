#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


def bin2str(bin_str: str, encoding: str = "utf-8") -> str:
    # Удаление всех символов кроме 0 и 1
    bin_str = "".join(c for c in bin_str if c in "01")

    h = hex(int(bin_str, 2))[2:]
    return bytes.fromhex(h).decode(encoding)


def str2bin(text: str, sep=" ", encoding: str = "utf-8") -> str:
    data: bytes = text.encode(encoding)

    # Example: 'You' -> '10110010110111101110101'
    bin_str = f"{int(data.hex(), 16):08b}"

    # Example: '10110010110111101110101 -> '01011001 01101111 01110101'
    bin_str = bin_str[::-1]
    items = [
        bin_str[i: i + 8][::-1].zfill(8)
        for i in range(0, len(bin_str), 8)
    ]
    items.reverse()

    return sep.join(items)


if __name__ == "__main__":
    assert str2bin("You") == "01011001 01101111 01110101"
    assert (
        str2bin(bin2str("01011001 01101111 01110101")) == "01011001 01101111 01110101"
    )
    assert str2bin(bin2str("010110010110111101110101")) == "01011001 01101111 01110101"

    assert bin2str("01011001 01101111 01110101") == "You"
    assert bin2str("010110010110111101110101") == "You"
    assert bin2str("01011001-01101111-01110101") == "You"
    assert bin2str("BIN: 01011001-01101111-01110101") == "You"

    assert bin2str(str2bin("You")) == "You"

    assert bin2str(str2bin("Привет")) == "Привет"

    print("Bin to text:")
    text = (
        "01011001 01101111 01110101 00100000 01100001 01110010 01100101 00100000 01101101 01101111 "
        "01110010 01100101 00100000 01110100 01101000 01100001 01101110 00100000 01101010 01110101 "
        "01110011 01110100 00100000 01100001 01101110 00100000 01100001 01101110 01101001 01101101 "
        "01100001 01101100 00101110"
    )
    print(bin2str(text))
    print()

    print("Text to bin:")
    text = "You are more than just an animal."
    print(str2bin(text))
