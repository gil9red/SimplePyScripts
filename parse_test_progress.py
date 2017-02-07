#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


def parse(text, append_test_case_list=True):
    total_value = 0
    total_max_value = 0

    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue

        if not append_test_case_list:
            import re
            line = re.sub('{#}:.*$', '{#}', line)
            line = line.strip()

        import re
        match = re.search(r'(\d+) +/ +(\d+)', line)
        value = int(match.group(1))
        max_value = int(match.group(2))

        total_value += value
        total_max_value += max_value

        line = line.replace('{#}', "({}%)".format(int(value / max_value * 100)))
        print(line)

    print()
    print("Total: {} / {} ({}%)".format(total_value, total_max_value, int(total_value / total_max_value * 100)))


if __name__ == '__main__':
    text = """
ATM - VSDC Issuing:         4  / 48 {#}: 9.1, 9.7, 9.8, 9.13
ATM - Magstripe Issuing:    4  / 4  {#}: 8.1, 8.7, 8.8, 12.1
Retail - VSDC Issuing:      0  / 13 {#}:
Retail - Magstripe Issuing: 4  / 4  {#}:
UCAT - Mag or VSDC Issuing: 2  / 2  {#}:
T&E - Mag or VSDC Issuing:  2  / 2  {#}:
CNP - Key-Entered Issuing:  15 / 15 {#}: 1.1, 3.1, 3.2, 3.3, 4.1, 4.2, 9.1, 9.3, 12.1, 12.4, 12.5, 13.1, 13.2, 16.4
Cash - Mag or VSDC Issuing: 5  / 5  {#}:
Payments - Issuing:         0  / 6  {#}:
"""

    parse(text, append_test_case_list=False)
    print('\n')
    parse(text)
