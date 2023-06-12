#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from psutil import process_iter, Process


def is_found(p: Process) -> bool:
    return "java" in p.name()


def is_server(p: Process) -> bool:
    return is_found(p) and "org.radixware.kernel.server.Server" in p.cmdline()


def is_explorer(p: Process) -> bool:
    return is_found(p) and "org.radixware.kernel.explorer.Explorer" in p.cmdline()


def kill_servers():
    for p in process_iter():
        if is_server(p):
            print(f"Kill server #{p.pid}")
            p.kill()


def kill_explorers():
    for p in process_iter():
        if is_explorer(p):
            print(f"Kill explorer #{p.pid}")
            p.kill()


if __name__ == "__main__":
    kill_servers()
    kill_explorers()
