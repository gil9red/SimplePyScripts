#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://ru.wikipedia.org/wiki/BMP
# SOURCE: https://en.wikipedia.org/wiki/BMP_file_format


import glob
import struct


# https://en.wikipedia.org/wiki/BMP_file_format#DIB_header_(bitmap_information_header)
SIZE_BY_HEADER_TYPE = {
    12: "BITMAPCOREHEADER / OS21XBITMAPHEADER",
    64: "OS22XBITMAPHEADER",
    16: "OS22XBITMAPHEADER",
    40: "BITMAPINFOHEADER",
    52: "BITMAPV2INFOHEADER",
    56: "BITMAPV3INFOHEADER",
    108: "BITMAPV4HEADER",
    124: "BITMAPV5HEADER",
}


def print_info(file_name: str):
    with open(file_name, "rb") as f:
        # Bitmap file header
        # BITMAPFILEHEADER
        bfType = f.read(2)
        print("bfType:", bfType)

        data = f.read(12)
        bfSize, bfReserved1, bfReserved2, bfOffBits = struct.unpack("<IHHI", data)
        print("bfSize:", bfSize)
        print("bfReserved1:", bfReserved1)
        print("bfReserved2:", bfReserved2)
        print("bfOffBits:", bfOffBits)

        # DIB header
        data = f.read(4)
        size = struct.unpack("<I", data)[0]
        print("size:", size)
        print("Header:", SIZE_BY_HEADER_TYPE.get(size, "<Unknown>"))


if __name__ == "__main__":
    for file_name in glob.glob("*.bmp"):
        print(file_name)
        print_info(file_name)
        print()
