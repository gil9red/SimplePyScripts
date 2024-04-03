#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import logging
import signal
import sys
import os
from logging.handlers import RotatingFileHandler
from pathlib import Path

import psutil


# SOURCE: https://psutil.readthedocs.io/en/latest/index.html#kill-process-tree
def kill_proc_tree(
    pid, sig=signal.SIGTERM, include_parent=True, timeout=None, on_terminate=None
):
    """Kill a process tree (including grandchildren) with signal
    "sig" and return a (gone, still_alive) tuple.
    "on_terminate", if specified, is a callback function which is
    called as soon as a child terminates.
    """
    assert pid != os.getpid(), "won't kill myself"
    parent = psutil.Process(pid)
    children = parent.children(recursive=True)
    if include_parent:
        children.append(parent)
    for p in children:
        try:
            p.send_signal(sig)
        except psutil.NoSuchProcess:
            pass
    gone, alive = psutil.wait_procs(children, timeout=timeout, callback=on_terminate)
    return gone, alive


def get_logger(
    name: str,
    fmt: str = "[%(asctime)s] %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s",
    file: str | Path = "main.log",
    encoding: str = "utf-8",
    log_stdout: bool = True,
    log_file: bool = True,
) -> "logging.Logger":
    log = logging.getLogger(name)
    log.setLevel(logging.DEBUG)

    formatter = logging.Formatter(fmt)

    if log_file:
        fh = RotatingFileHandler(
            file, maxBytes=10_000_000, backupCount=5, encoding=encoding
        )
        fh.setFormatter(formatter)
        log.addHandler(fh)

    if log_stdout:
        sh = logging.StreamHandler(stream=sys.stdout)
        sh.setFormatter(formatter)
        log.addHandler(sh)

    return log
