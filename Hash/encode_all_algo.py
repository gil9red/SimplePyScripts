#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import hashlib


available = list(set(map(str.lower, hashlib.algorithms_available)))
available.sort()

text = "hello world"

for algo_name in available:
    try:
        alg = hashlib.new(algo_name)  # create hash function from name
        alg.update(text.encode())  # set data in hash-function
        print(f"{algo_name}: {alg.hexdigest().upper()}")

    except ValueError:
        pass
