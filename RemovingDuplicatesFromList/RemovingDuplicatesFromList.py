# coding=utf-8

__author__ = "ipetrash"


import argparse


def create_parser():
    parser = argparse.ArgumentParser(description="Removing duplicates from a list")
    return parser


if __name__ == "__main__":
    create_parser().parse_args()
    list = input("Enter a list of elements separated by a space: ").split(" ")
    list = list(filter(None, list))
    print("Source list: %s" % list)
    list.sort()
    print("Sorted list: %s" % list)
    for x in list:
        if list.count(x) > 1:
            list.remove(x)
    print("Result: %s" % list)
    print("List: " + ", ".join(list))
