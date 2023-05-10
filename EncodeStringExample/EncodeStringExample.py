# coding=utf-8
import argparse

__author__ = "ipetrash"


def create_parser():
    parse = argparse.ArgumentParser(
        description="Output a user-defined string in different encodings."
    )
    return parse


if __name__ == "__main__":
    create_parser().parse_args()

    string = input("text = ")
    list_encoding = {
        "windows-1251",
        "UTF-16",
        "UTF-16LE",
        "UTF-16BE",
        "ASCII",
        "Latin-1",
    }
    for encoding in list_encoding:
        print(f"{encoding}: {string.encode(encoding)}")
