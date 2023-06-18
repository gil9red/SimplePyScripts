#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://stackoverflow.com/a/39186313/5909792


from abc import ABC


def singleton(real_cls):
    class SingletonFactory(ABC):
        instance = None

        def __new__(cls, *args, **kwargs):
            if not cls.instance:
                cls.instance = real_cls(*args, **kwargs)
            return cls.instance

    SingletonFactory.register(real_cls)
    return SingletonFactory


if __name__ == "__main__":

    @singleton
    class MyClass:
        pass

    x1 = MyClass()
    x2 = MyClass()
    x3 = MyClass()

    print(id(x1), id(x2), id(x3), id(MyClass.instance))
    assert id(x1) == id(x2) == id(x3) == id(MyClass.instance)
