#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://www.python.org/dev/peps/pep-0318/#examples


def singleton(cls):
    instances = dict()

    def get_instance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]

    return get_instance


if __name__ == "__main__":

    @singleton
    class MyClass:
        pass

    x1 = MyClass()
    x2 = MyClass()
    x3 = MyClass()

    print(id(x1), id(x2), id(x3))
