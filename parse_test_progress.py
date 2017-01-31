#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


def parse(text):
    total_value = 0
    total_max_value = 0

    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue

        import re
        match = re.search(r'(\d+) +/ +(\d+)', line)
        value = int(match.group(1))
        max_value = int(match.group(2))

        total_value += value
        total_max_value += max_value

        print(line + " ({}%)".format(int(value / max_value * 100)))

    print()
    print("Total: {} / {} ({}%)".format(total_value, total_max_value, int(total_value / total_max_value * 100)))


if __name__ == '__main__':
    text = """
ATM - VSDC Issuing:         4  / 48
ATM - Magstripe Issuing:    0  / 4
Retail - VSDC Issuing:      0  / 13
Retail - Magstripe Issuing: 4  / 4
UCAT - Mag or VSDC Issuing: 2  / 2
T&E - Mag or VSDC Issuing:  2  / 2
CNP - Key-Entered Issuing:  15 / 15
Cash - Mag or VSDC Issuing: 5  / 5
Payments - Issuing:         0  / 6
"""

    parse(text)
