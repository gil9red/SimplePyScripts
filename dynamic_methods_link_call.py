#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


class CallBuilder:
    def __init__(self, part=None, sep="") -> None:
        self._part = part
        self._sep = sep

    def __getattr__(self, part):
        return CallBuilder(
            part=((self._part + self._sep) if self._part else "") + part,
            sep=self._sep,
        )

    def __call__(self, **kwargs):
        return self._part


if __name__ == "__main__":
    builder = CallBuilder()
    result = builder.H.e.l.l.o._.World()
    print(result)  # Hello_World

    builder = CallBuilder(sep=".")
    result = builder.H.e.l.l.o._.World()
    print(result)  # H.e.l.l.o._.World

    builder = CallBuilder(sep=".")
    result = builder.H.e.l.l.o._.W.o.r.l.d()
    print(result)  # H.e.l.l.o._.W.o.r.l.d
