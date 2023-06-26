#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import hashlib

# pip install simpleeval
from simpleeval import SimpleEval

from simple_eval__hashlib__fill_functions import hashlib_func


class SimpleHashlibEval(SimpleEval):
    def _eval_call(self, node):
        name = node.func.id.lower()

        # Case-insensitive call func and check argument
        if name in hashlib.algorithms_guaranteed and node.args:
            value = self._eval(node.args[0])
            return hashlib_func(value, name)

        return super()._eval_call(node)


if __name__ == "__main__":
    hashlib_eval = SimpleHashlibEval()

    print(hashlib_eval.eval('md5("Hello World!")')) # ed076287532e86365e841e92bfc50d8c
    print(
        hashlib_eval.eval('sha1("Hello World!")')
    )  # 2ef7bde608ce5404e97d5f042f95f89f1c232871
    print(
        hashlib_eval.eval('sha256("Hello World!")')
    )  # 7f83b1657ff1fc53b92dc18148a1d65dfc2d4b1fa3d677284addd200126d9069
    print()

    print(
        hashlib_eval.eval('md5(md5("Hello World!"))')
    )  # 153163e20c7dd03b131fe2bf21927e1e
    print(
        hashlib_eval.eval('md5(md5("Hello") + md5("World!"))')
    )  # 72a6d987a2848481595dba5ea4426b6e
    print()

    print(
        hashlib_eval.eval('md5("Hello World!" + "my_secret_salt")')
    )  # 9ee8e345639a8f7d51853eb459abaa81
    print()

    print(hashlib_eval.eval('MD5("Hello World!")'))  # ed076287532e86365e841e92bfc50d8c
    print(hashlib_eval.eval('mD5("Hello World!")'))  # ed076287532e86365e841e92bfc50d8c
