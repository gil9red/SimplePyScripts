# coding=utf-8

__author__ = "ipetrash"


import argparse


def create_parser():
    parser = argparse.ArgumentParser(
        description="Find the longest word in a string, separated by spaces."
    )
    return parser


if __name__ == "__main__":
    create_parser().parse_args()

    string = input("Input string: ")
    max_len = -1
    max_len_word = ""
    for word in string.split(" "):
        current_len = len(word)
        if current_len > max_len:
            max_len = current_len
            max_len_word = word

    print("Longest word: " + max_len_word)
