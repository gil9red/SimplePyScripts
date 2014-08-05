# coding=utf-8
import argparse

__author__ = 'ipetrash'


def create_parser():
    parser = argparse.ArgumentParser(description="The table of multiplication by M. Table compiled from M * a, to M * b, "
                                                 "where M, a, b are requested from the user.")
    return parser


if __name__ == '__main__':
    create_parser().parse_args()

    M = int(raw_input("M="))
    a = int(raw_input("a="))
    b = int(raw_input("b="))
    for x in range(a, b):
        print("%d * %d = %d" % (M, x, M * x))
