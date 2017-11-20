#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


def attrs(**kwargs):
    def decorate(f):
        for k in kwargs:
            setattr(f, k, kwargs[k])
        return f

    return decorate


@attrs(versionadded="2.2", author="Guido van Rossum")
class Foo:
    pass


print(Foo.author)  # Guido van Rossum
print(Foo().author)  # Guido van Rossum
print(list(filter(lambda x: not x.startswith('_'), dir(Foo()))))  # ['author', 'versionadded']
