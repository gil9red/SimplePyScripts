#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: http://vip.sugovica.hu/Sardi/kepnezo/JPEG%20File%20Layout%20and%20Format.htm
# SOURCE: https://en.wikipedia.org/wiki/JPEG#Syntax_and_structure


import glob
import struct


def print_info(file_name: str) -> None:
    print(file_name)

    with open(file_name, "rb") as f:
        # JFIF APP0

        # Read SOI
        data = f.read(2)

        if data != b"\xff\xd8":
            print("Not valid JPEG!")
            return

        # APP0 marker FF E0
        marker_APP0 = f.read(2)

        # Length
        f.read(2)

        # Identifier. b'JFIF\x00'
        data = f.read(5)

        # Find 0xff, 0xc0 to identify SOF0 marker
        while data:
            data = f.read(1)
            if data == b"\xff" and f.read(1) == b"\xc0":
                break

        # This value equals to 8 + components*3 value
        (length,) = struct.unpack(">H", f.read(2))
        # print('Length:', length)

        # This is in bits/sample, usually 8 (12 and 16 not supported by most software).
        (data_precision,) = struct.unpack(">b", f.read(1))
        # print('Data precision:', data_precision)

        height, width = struct.unpack(">HH", f.read(4))
        print(f"    Size: {width}x{height}")

        # Usually 1 = grey scaled, 3 = color YcbCr or YIQ 4 = color CMYK
        (number_of_components,) = struct.unpack(">b", f.read(1))
        # print('Number of components:', number_of_components)

        # Each component:
        #   component Id(1byte): (1 = Y, 2 = Cb, 3 = Cr, 4 = I, 5 = Q)
        #   sampling factors (1byte) (bit 0-3 vertical., 4-7 horizontal.)
        #   quantization table number (1 byte)
        component_id, sampling_factors, quantization_table_number = struct.unpack(
            ">bbb", f.read(3)
        )
        # print('Component id:', component_id)
        # print('Sampling factors:', sampling_factors)
        # print('Quantization table number:', quantization_table_number)


if __name__ == "__main__":
    for file_name in glob.glob("*.jpg") + glob.glob("*.jpeg"):
        print_info(file_name)
        print()
