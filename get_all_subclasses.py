#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://stackoverflow.com/a/17246726/5909792
def get_all_subclasses(cls):
    all_subclasses = []

    for subclass in cls.__subclasses__():
        all_subclasses.append(subclass)
        all_subclasses.extend(get_all_subclasses(subclass))

    return all_subclasses


if __name__ == "__main__":

    class A:
        name = "A"

    class B(A):
        name = "AB"

    class C(A):
        name = "AC"

    class D(C):
        name = "ACD"

    class E(C):
        name = "ACE"

    class F(D):
        name = "ACDF"

    print(get_all_subclasses(A))
    # [<class '__main__.B'>, <class '__main__.C'>, <class '__main__.D'>,...

    print(get_all_subclasses(B))
    # []

    print(get_all_subclasses(C))
    # [<class '__main__.D'>, <class '__main__.F'>, <class '__main__.E'>]
