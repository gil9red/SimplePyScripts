#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import rsa
from utils import FILE_NAME_PUBLIC_KEY, FILE_NAME_PRIVATE_KEY


print(
    f"The {repr(FILE_NAME_PUBLIC_KEY)} or {repr(FILE_NAME_PRIVATE_KEY)} files are empty! "
    f"Performing key generation!"
)

public_key, private_key = rsa.new_keys(key_size=2048)
print("Key generation completed successfully!")

with open(FILE_NAME_PUBLIC_KEY, "wb") as f:
    f.write(public_key.exportKey("PEM"))

with open(FILE_NAME_PRIVATE_KEY, "wb") as f:
    f.write(private_key.exportKey("PEM"))

print("Successfully save generated keys to files!")
