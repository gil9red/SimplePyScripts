# coding=utf-8

import argparse

__author__ = 'ipetrash'


def create_parser():
    parser = argparse.ArgumentParser(description="Read URLs from file with URL.")
    return parser

if __name__ == '__main__':
    create_parser().parse_args()
    file_path = raw_input("Input file path: ")
    file = open(file_path, "r")
    for line in file.readlines():
        print(line)
    file.close()