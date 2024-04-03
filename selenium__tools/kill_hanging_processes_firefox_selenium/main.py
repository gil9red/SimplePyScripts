#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import psutil
from common import get_logger, kill_proc_tree


log = get_logger(__file__)


for p in psutil.process_iter():
    try:
        if p.name() != "firefox.exe":
            continue

        if "--marionette" not in p.cmdline():
            continue

        parent_names: list[str] = [p.name() for p in p.parents()]
        if "geckodriver.exe" in parent_names:
            continue

        log.info(f"Kill {p}")
        kill_proc_tree(p.pid)

    except (psutil.NoSuchProcess, psutil.AccessDenied):
        pass
