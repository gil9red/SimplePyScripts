#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


def attrs(**kwargs):
    def decorate(f):
        for k in kwargs:
            setattr(f, k, kwargs[k])
        return f

    return decorate


@attrs(versionadded="2.2", author="Guido van Rossum")
def mymethod(text="ok"):
    return text


print(mymethod.author)  # Guido van Rossum
print(mymethod())  # ok
print(mymethod("no"))  # ok
