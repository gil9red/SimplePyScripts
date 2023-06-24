#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


class MyMeta(type):
    instances = list()

    def __call__(cls, *args, **kwargs):
        instance = super(MyMeta, cls).__call__(*args, **kwargs)
        cls.instances.append(instance)

        return instance


# Python2
class MyClass(object):
    __metaclass__ = MyMeta


# Python3
class MyClass(object, metaclass=MyMeta):
    pass


print(MyClass.instances)  # []
a = MyClass()
print(MyClass.instances)  # [<__main__.MyClass object at 0x00514AF0>]
b = MyClass()
c = MyClass()
print(MyClass.instances)
# [<__main__.MyClass object at 0x00514AF0>, <__main__.MyClass object at 0x00736DF0>, <__main__.MyClass object at 0x00736C30>]
