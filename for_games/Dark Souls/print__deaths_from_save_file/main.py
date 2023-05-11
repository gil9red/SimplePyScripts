#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import struct


# SOURCE: analog dsfp ("import dsfp") / https://github.com/tarvitz/dsfp
# SOURCE: https://github.com/RKYates/Dark-Souls-Death-Count-cgi-page/blob/master/cgi-bin/results.py


def get_chars_and_deaths(file_name: str) -> list:
    chars = []

    with open(file_name, "rb") as f:
        f.seek(0x2C0, 0)

        for slot in range(0, 10):
            f.seek(0x100, 1)
            name = f.read(32)

            if name[0] != "\00":
                f.seek(-0x120, 1)
                f.seek(0x1F128, 1)
                deaths = f.read(4)
                f.seek(-0x04, 1)
                f.seek(-0x1F128, 1)
                char_name = name.decode("utf-16").split("\00")[0]
                char_deaths = struct.unpack("i", deaths)[0]
                if char_name:
                    chars.append((char_name, char_deaths))
            else:
                f.seek(-0x120, 1)

            f.seek(0x60190, 1)

    return chars


if __name__ == "__main__":
    # C:\Users\<CURRENT_USER>\Documents\NBGI\DarkSouls\<PLAYER_NAME>\DRAKS0005.sl2
    file_name = "DRAKS0005.sl2"

    chars = get_chars_and_deaths(file_name)
    for name, deaths in chars:
        print(f"{name}, deaths: {deaths}")

    print()

    # Find and print from local
    import os
    from glob import glob

    path = os.path.expanduser(r"~\Documents\NBGI\DarkSouls\*\DRAKS0005.sl2")
    for file_name in glob(path):
        print(file_name)

        chars = get_chars_and_deaths(file_name)
        for name, deaths in chars:
            print(f"    {name}, deaths: {deaths}")
