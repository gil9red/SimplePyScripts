#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# http://stackoverflow.com/questions/35332611/a-program-which-creates-emails


def fill_list(l, promt) -> None:
    while True:
        x = input(promt)
        if not x:
            break

        l.append(x)


if __name__ == "__main__":
    first_names = list()
    last_names = list()

    fill_list(first_names, "Input first name: ")
    print(f"first_names: {first_names}")

    fill_list(last_names, "Input last name: ")
    print(f"last_names: {last_names}")

    for first, last in zip(first_names, last_names):
        print(f"{first}.{last}@abc.mail.com")
