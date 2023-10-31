#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# pip install psutil
import psutil


for process in psutil.process_iter():
    if "conemu64" in process.name().lower():
        children = process.children(recursive=True)
        print(
            f"Kill process. Pid={process.pid}, name={process.name()}, children: {len(children)}"
        )

        # Если убивать только процесс, то его дочерние процессы останутся как отдельные окна консоли
        for child in children:
            child.kill()

        process.kill()
