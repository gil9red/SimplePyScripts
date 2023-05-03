#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: Design Patterns: Prototype - Прототип
# SOURCE: https://ru.wikipedia.org/wiki/Прототип_(шаблон_проектирования)#Пример_на_Python


import copy


class Prototype:
    def __init__(self):
        self._objects = dict()

    def register_object(self, name, obj):
        """Register an object"""
        self._objects[name] = obj

    def unregister_object(self, name):
        """Unregister an object"""
        self._objects.pop(name)

    def clone(self, name, **attr):
        """Clone a registered object and update inner attributes dictionary"""
        obj = copy.deepcopy(self._objects.get(name))
        obj.__dict__.update(attr)
        return obj


if __name__ == "__main__":

    class A:
        def __init__(self):
            self.x = 3
            self.y = 8
            self.z = 15
            self.garbage = [38, 11, 19]

        def __str__(self):
            return f"A({self.x}, {self.y}, {self.z}, {self.garbage})"

    a = A()

    prototype = Prototype()
    prototype.register_object("object_a", a)

    b = prototype.clone("object_a")
    c = prototype.clone("object_a", x=1, y=2, garbage=[88, 1])

    for x in (a, b, c):
        print(x)

    # A(3, 8, 15, [38, 11, 19])
    # A(3, 8, 15, [38, 11, 19])
    # A(1, 2, 15, [88, 1])
