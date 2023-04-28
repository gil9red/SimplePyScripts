#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


def attrs(**kwargs):
    def decorate(cls):
        for k in kwargs:
            setattr(cls, k, kwargs[k])

        return cls

    return decorate


@attrs(version="2.2", author="Guido van Rossum")
class Foo:
    pass


print(Foo.author)     # Guido van Rossum
print(Foo().author)   # Guido van Rossum
print(Foo().version)  # 2.2
print(
    list(filter(lambda x: not x.startswith("_"), dir(Foo())))
)
# ['author', 'version']
