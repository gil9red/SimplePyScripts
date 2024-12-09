#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from pathlib import Path
from psutil import process_iter, Process, Error


def is_found(p: Process, cwd: str | Path) -> bool:
    if isinstance(cwd, str):
        cwd = Path(cwd)
    return cwd.exists() and Path(p.cwd()).is_relative_to(cwd)


def get_processes(cwd: str | Path = None) -> list[Process]:
    items = []
    for p in process_iter():
        try:
            if is_found(p, cwd):
                items.append(p)
        except Error:
            pass
    return items


# TODO: Вывести деревом список процессов
for p in get_processes(r"C:\DEV__TX\trunk"):
    print(p, p.cwd(), p.name(), p.cmdline(), p.parent())

# TODO: Алгоритм преобразования список в дерево
