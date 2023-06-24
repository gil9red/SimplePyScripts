#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


class MyMeta(type):
    def __new__(cls, name, bases, attrs):
        print(f"{name}, initialize={attrs['initialize']}")

        if attrs["initialize"]:
            attrs["SUPER_VALUE"] = 42
            attrs["run"] = lambda self=None: print("run!")

        attrs["reverse_initialize"] = not attrs["initialize"]

        return super().__new__(cls, name, bases, attrs)


class A(metaclass=MyMeta):
    initialize = False


class B(A):
    initialize = True


print(hasattr(A, "SUPER_VALUE"))  # False
print(hasattr(B, "SUPER_VALUE"))  # True
print()

print(A.initialize, A.reverse_initialize)  # False True
print(B.initialize, B.reverse_initialize)  # True False
print()

print(B.SUPER_VALUE)  # 42
B.run()  # run!

b = B()
print(b.SUPER_VALUE)  # 42
b.run()  # run!
