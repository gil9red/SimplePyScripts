#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import hashlib

# pip install simpleeval
from simpleeval import SimpleEval


def hashlib_func(value, algo_name):
    data = bytes(str(value), "utf-8")
    return hashlib.new(algo_name, data).hexdigest()


class SimpleHashlibEval(SimpleEval):
    def __init__(self):
        functions = dict()

        for algo_name in hashlib.algorithms_guaranteed:
            functions[algo_name] = lambda value, algo_name=algo_name: hashlib_func(
                value, algo_name
            )

        super().__init__(functions=functions)


if __name__ == "__main__":
    hashlib_eval = SimpleHashlibEval()

    print(hashlib_eval.eval('md5("Hello World!")'))
    # ed076287532e86365e841e92bfc50d8c
    print(
        hashlib_eval.eval('sha1("Hello World!")')
    )
    # 2ef7bde608ce5404e97d5f042f95f89f1c232871
    print(
        hashlib_eval.eval('sha256("Hello World!")')
    )
    # 7f83b1657ff1fc53b92dc18148a1d65dfc2d4b1fa3d677284addd200126d9069
    print()

    print(
        hashlib_eval.eval('md5(md5("Hello World!"))')
    )
    # 153163e20c7dd03b131fe2bf21927e1e
    print(
        hashlib_eval.eval('md5(md5("Hello") + md5("World!"))')
    )
    # 72a6d987a2848481595dba5ea4426b6e
    print()

    print(
        hashlib_eval.eval('md5("Hello World!" + "my_secret_salt")')
    )
    # 9ee8e345639a8f7d51853eb459abaa81
