#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import ctypes


def main():
    i = ctypes.c_char('a'.encode())
    j = ctypes.pointer(i)
    j[99] = 'a'.encode()
    # Process finished with exit code -1073741819 (0xC0000005)


if __name__ == "__main__":
    main()
