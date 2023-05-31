#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import argparse


def create_parser():
    parser = argparse.ArgumentParser(
        description="The table of multiplication by M. Table compiled from M * a, to M * b, "
        "where M, a, b are requested from the user."
    )
    return parser


if __name__ == "__main__":
    create_parser().parse_args()

    M = int(input("M="))
    a = int(input("a="))
    b = int(input("b="))
    for x in range(a, b):
        print(f"{M:d} * {x:d} = {M * x:d}")
