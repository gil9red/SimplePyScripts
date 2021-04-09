#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from timeit import timeit


foo = 'FooBar'
test_globals = dict(foo=foo)

t = timeit('name = "Thread #" + foo', globals=test_globals)
print(f'Total time: {t:.3f} sec')

t = timeit('name = "Thread #%s" % foo', globals=test_globals)
print(f'Total time: {t:.3f} sec')

t = timeit('name = "Thread #{}".format(foo)', globals=test_globals)
print(f'Total time: {t:.3f} sec')

t = timeit('name = f"Thread {foo}"', globals=test_globals)
print(f'Total time: {t:.3f} sec')

"""
Total time: 0.077 sec
Total time: 0.179 sec
Total time: 0.244 sec
Total time: 0.081 sec
"""
