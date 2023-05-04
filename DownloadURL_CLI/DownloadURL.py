# coding=utf-8

__author__ = "ipetrash"


import argparse
from urllib.request import urlopen


def create_parser():
    parser = argparse.ArgumentParser(description="Download content URL.")
    return parser


if __name__ == "__main__":
    create_parser().parse_args()
    url = input("Input url: ")
    file = urlopen(url)
    content = file.read()
    print(content)
