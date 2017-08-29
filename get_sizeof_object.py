#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# SOURCE: https://code.activestate.com/recipes/577504

from __future__ import print_function
from sys import getsizeof, stderr
from itertools import chain
from collections import deque

try:
    from reprlib import repr
except ImportError:
    pass


def total_size(o, handlers={}, verbose=False):
    """ Returns the approximate memory footprint an object and all of its contents.

Automatically finds the contents of the following builtin containers and
their subclasses: tuple, list, deque, dict, set and frozenset.
To search other containers, add handlers to iterate over their contents:

handlers = {SomeContainerClass: iter,
OtherContainerClass: OtherContainerClass.get_elements}

"""
    dict_handler = lambda d: chain.from_iterable(d.items())
    all_handlers = {tuple: iter,
                    list: iter,
                    deque: iter,
                    dict: dict_handler,
                    set: iter,
                    frozenset: iter,
                    }
    all_handlers.update(handlers)  # user handlers take precedence
    seen = set()  # track which object id's have already been seen
    default_size = getsizeof(0)  # estimate sizeof object without __sizeof__

    def sizeof(o):
        if id(o) in seen:  # do not double count the same object
            return 0
        seen.add(id(o))
        s = getsizeof(o, default_size)

        if verbose:
            print(s, type(o), repr(o), file=stderr)

        for typ, handler in all_handlers.items():
            if isinstance(o, typ):
                s += sum(map(sizeof, handler(o)))
                break
        return s

    return sizeof(o)


if __name__ == '__main__':
    d = dict(a=1, b=2, c=3, d=[4, 5, 6, 7], e='a string of chars')
    print(total_size(d, verbose=True))

    print(total_size(None))
    print(total_size(3))
    print(total_size(2**63))
    print(total_size(102947298469128649161972364837164))
    print(total_size(918659326943756134897561304875610348756384756193485761304875613948576297485698417))
    print(total_size(""))
    print(total_size("My hovercraft is full of eels"))
    print(total_size([]))
    print(total_size([4, "toaster", 230.1]))
    print(total_size({}))
    print(total_size({'a': 213, 'b': 2131}))
