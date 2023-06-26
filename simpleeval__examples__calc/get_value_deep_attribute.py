#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# pip install simpleeval
import simpleeval


class Foo:
    class A:
        class B:
            class C:
                value = 3

        value = 25


my_eval = simpleeval.SimpleEval()
my_eval.names["foo"] = Foo

print(my_eval.eval("foo.A.B.C.value * 10 + foo.A.value"))  # 55
