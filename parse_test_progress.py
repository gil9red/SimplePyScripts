#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import re


def parse(text, append_test_case_list=True):
    total_value = 0
    total_max_value = 0

    for line in text.splitlines():
        line = line.rstrip()
        if not line:
            print(line)
            continue

        match = re.search(r"{@} +/ +(\d+)", line)
        if not match:
            print(line)
            continue

        max_value = int(match.group(1))

        match = re.search("{#}:(.*)$", line)
        if match:
            # Получение списка значений
            values = match.group(1).split(",")

            # Удаление пустых символов
            values = map(str.strip, values)

            # Удаление пустых строк
            values = filter(lambda x: x, values)

            # Удаление дупликатов
            value = len(set(values))
        else:
            value = 0

        total_value += value
        total_max_value += max_value

        line = line.replace("{@}", str(value))
        line = line.replace("{#}", f"({int(value / max_value * 100)}%)")

        if not append_test_case_list:
            index = line.rfind(":")
            if index != -1:
                line = line[:index]

        print(line)

    print()
    print(
        f"Итого: {total_value} / {total_max_value} ({int(total_value / total_max_value * 100)}%)"
    )


if __name__ == "__main__":
    text = """\
Набивка тестов:
ATM - VSDC Issuing:         {@}  / 48 {#}:
ATM - Magstripe Issuing:    {@}  / 4  {#}: 8.1, 8.7, 8.8, 12.1
Retail - VSDC Issuing:      {@}  / 13 {#}:
Retail - Magstripe Issuing: {@}  / 4  {#}: 2.1, 2.3, 3.1, 7.1
UCAT - Mag or VSDC Issuing: {@}  / 2  {#}: 2.3, 6.1
T&E - Mag or VSDC Issuing:  {@}  / 2  {#}: 1.2, 1.3
CNP - Key-Entered Issuing:  {@} / 15 {#}: 1.1, 3.1, 3.2, 3.3, 4.1, 4.2, 9.1, 9.3, 12.1, 12.4, 12.5
Cash - Mag or VSDC Issuing: {@}  / 5  {#}: 1.1, 1.2, 1.3, 1.4, 2.1
Payments - Issuing:         {@}  / 6  {#}: 3.1, 3.3, 3.4, 6.1, 6.3, 6.4
"""

    # parse(text, append_test_case_list=False)
    # print('\n')
    parse(text)
