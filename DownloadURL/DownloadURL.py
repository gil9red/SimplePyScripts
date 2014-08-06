# coding=utf-8

import argparse
import urllib2

__author__ = 'ipetrash'


def create_parser():
    parser = argparse.ArgumentParser(description="Download content URL.")
    return parser

if __name__ == '__main__':
    create_parser().parse_args()
    url = raw_input("Input url: ")
    file = urllib2.urlopen(url)
    content = file.read()
    print(content)