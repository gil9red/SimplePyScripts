# coding=utf-8

__author__ = "ipetrash"


import argparse


def create_parser():
    parser = argparse.ArgumentParser(description="Read URLs from file with URL.")
    return parser


if __name__ == "__main__":
    create_parser().parse_args()
    file_path = input("Input file path: ")
    with open(file_path) as f:
        for line in f.readlines():
            print(line)
