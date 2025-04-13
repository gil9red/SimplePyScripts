#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import re
from subprocess import Popen, PIPE


def pc_name(ip: str) -> str | None:
    """Функция для получения имени компьютера по ip."""

    with Popen(
        ["nslookup", ip], universal_newlines=True, stdout=PIPE, stderr=PIPE
    ) as p:
        if not p.stderr.read():
            text = p.stdout.read()
            if m := re.search(r"Name:(.+)", text):
                return m.group(1).strip()


if __name__ == "__main__":
    from itertools import product

    with open("ip_pc_name", mode="w", encoding="utf-8") as f:
        for i, j, k, m in product(range(256), repeat=4):
            ping = f"{i}.{j}.{k}.{m}"
            name = pc_name(ping)

            if name is not None:
                print(ping, name)
                print(ping, name, file=f)
