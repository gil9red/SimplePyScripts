#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import hashlib
import sys


algorithms = list(hashlib.algorithms_available)  # get list algorithms
algorithms.sort()
print(f"Algorithms available: {', '.join(algorithms)}")

text = input("Text: ")
if not text:
    print("Empty text!")
    sys.exit(1)

alg_name = input("Name algorithm: ")
if alg_name not in algorithms:  # search in list
    print("Algorithm not found!")
    sys.exit(1)

alg = hashlib.new(alg_name)  # create hash function from name
alg.update(text.encode())  # set data in hash-function
print("Result:")
print(f" hex: {alg.hexdigest()}")
print(f" HEX: {alg.hexdigest().upper()}")
