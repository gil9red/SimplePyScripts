#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from psutil import process_iter, Process


def is_server(p: Process) -> bool:
    return "org.radixware.kernel.server.Server" in p.cmdline()


def is_explorer(p: Process) -> bool:
    return "org.radixware.kernel.explorer.Explorer" in p.cmdline()


def get_processes() -> list[Process]:
    items = []
    for p in process_iter():
        if "java" not in p.name():
            continue

        if is_server(p) or is_explorer(p):
            items.append(p)

    return items


def kill_servers():
    for p in get_processes():
        if is_server(p):
            print(f"Kill server #{p.pid}")
            p.kill()


def kill_explorers():
    for p in get_processes():
        if is_explorer(p):
            print(f"Kill explorer #{p.pid}")
            p.kill()


if __name__ == "__main__":
    kill_servers()
    kill_explorers()
