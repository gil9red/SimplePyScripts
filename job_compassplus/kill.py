#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from pathlib import Path
from psutil import process_iter, Process, Error


def is_found(p: Process, cwd: str | Path = None) -> bool:
    if isinstance(cwd, str):
        cwd = Path(cwd)
    if cwd:
        is_equal_path = cwd.exists() and cwd == Path(p.cwd())
    else:
        is_equal_path = True

    return "java" in p.name() and is_equal_path


def get_processes(cwd: str | Path = None) -> list[Process]:
    items = []
    for p in process_iter():
        try:
            if is_found(p, cwd):
                items.append(p)
        except Error:
            pass
    return items


def is_server(p: Process) -> bool:
    return "org.radixware.kernel.server.Server" in p.cmdline()


def is_explorer(p: Process) -> bool:
    return "org.radixware.kernel.explorer.Explorer" in p.cmdline()


def kill_servers(cwd: str | Path = None):
    for p in get_processes(cwd):
        if is_server(p):
            print(f"Kill server #{p.pid}")
            p.kill()


def kill_explorers(cwd: str | Path = None):
    for p in get_processes(cwd):
        if is_explorer(p):
            print(f"Kill explorer #{p.pid}")
            p.kill()


if __name__ == "__main__":
    kill_servers()
    kill_explorers()
