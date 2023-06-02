#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: Чтобы узнать кто какие занял/прослушивает порты


from subprocess import check_output


# SOURCE: https://github.com/gil9red/SimplePyScripts/blob/c24fb90f1c6b792ebd77e2f916ef5ec7d741c494/ascii_table__simple_pretty__rjust.py
def print_pretty_table(data, cell_sep=" | "):
    rows = len(data)
    cols = len(data[0])

    col_width = []
    for col in range(cols):
        columns = [data[row][col] for row in range(rows)]
        col_width.append(len(max(columns, key=len)))

    header_ok = False

    for row in range(rows):
        result = []
        for col in range(cols):
            item = data[row][col].rjust(col_width[col])
            result.append(item)

        print(cell_sep.join(result))

        # Append header separate
        if not header_ok:
            print(" + ".join("-" * width for width in col_width))
            header_ok = True


def get_raw_data() -> str:
    cmd = "netstat -ano -p tcp"
    return check_output(cmd, universal_newlines=True).strip()


def get_data() -> tuple[list, list]:
    text = get_raw_data()
    lines = text.split("\n")[3:]

    headers = ["Proto", "Local Address", "Foreign Address", "State", "PID"]
    return headers, [line.split() for line in lines]


if __name__ == "__main__":
    print(get_raw_data())

    print("\n\n")

    headers, rows = get_data()

    data = [list(map(str.upper, headers))]
    data += rows

    print_pretty_table(data)
