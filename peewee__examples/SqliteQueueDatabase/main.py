#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import concurrent.futures
import db


def create_parameter(name: str, value: str) -> db.Parameter:
    return db.Parameter.add(name, value)


with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    N = 10000

    futures = [
        executor.submit(create_parameter, f"name_{i}", f"value_{i}")
        for i in range(N)
    ]

    items = []
    for future in concurrent.futures.as_completed(futures):
        data: db.Parameter = future.result()
        items.append(data)

    print("items:", len(items))
    print("count:", db.Parameter.count())
    assert len(items) == N
