#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://ru.stackoverflow.com/a/776977/201445


import binascii
import hashlib
import itertools
import multiprocessing
import string

from functools import partial


alphabet = (string.ascii_letters + string.digits).encode()


def sha256(data):
    return hashlib.sha256(data).digest()


def check_sha256(repls_parent, bytes_format, n, target_sha256):
    for repls in itertools.product(alphabet, repeat=n):
        data = bytes_format % (repls_parent + repls)
        if sha256(data) == target_sha256:
            return data


def brute_force(mask, target_sha256, n_cutoff=4):
    """
    n_cutoff -- number of `*` to process in a worker process
    """

    target_sha256 = binascii.unhexlify(target_sha256)

    bytes_format = mask.replace(b"%", b"%%").replace(b"*", b"%c")
    mp_check = partial(
        check_sha256,
        bytes_format=bytes_format,
        n=min(n_cutoff, mask.count(b"*")),
        target_sha256=target_sha256,
    )
    n = max(0, mask.count(b"*") - n_cutoff)
    all_repls_parent = itertools.product(alphabet, repeat=n)
    with multiprocessing.Pool() as pool:
        for data in pool.imap_unordered(mp_check, all_repls_parent):
            if data is not None:
                return data


if __name__ == "__main__":
    # Password: qwe12y
    sha256_hex = b"b8cc184b3f4aeb6adb6601ea3e39ef5ac098791acc2a505a66746f43d0c7ed85"

    passw_bytes = brute_force(b"qw****", sha256_hex)
    print(passw_bytes.decode())
