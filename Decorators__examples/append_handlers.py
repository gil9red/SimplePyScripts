#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from collections import defaultdict


class Collector:
    def __init__(self) -> None:
        self.handlers = []
        self.handlers_by_name = defaultdict(list)

    def add(self, name="default"):
        def decorator(func):
            self.handlers.append(func)
            self.handlers_by_name[name].append(func)

            return func

        return decorator


collector = Collector()


@collector.add(name="test")
def hello_world(end="!") -> None:
    print("hello world" + end)


print(collector.handlers)  # [<function hello_world at 0x002A6738>]
print(collector.handlers_by_name)
# defaultdict(<class 'list'>, {'test': [<function hello_world at 0x00310198>]})

hello_world("!!!")  # hello world!!!
hello_world()  # hello world!
print(collector.handlers)  # [<function hello_world at 0x002A6738>]
collector.handlers[0]()  # hello world!


@collector.add(name="this it say_hello!")
def say_hello() -> None:
    print("hello!")


print()
print(collector.handlers)
# [<function hello_world at 0x002A6738>, <function say_hello at 0x007010C0>]
print(len(collector.handlers_by_name))  # 2
for func in collector.handlers:
    func()
