#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://stackoverflow.com/a/55026299/5909792


# code from https://utcc.utoronto.ca/~cks/space/blog/python/GetAllObjects
import gc


# Recursively expand slist's objects
# into olist, using seen to track
# already processed objects.
def _getr(slist, olist, seen):
    for e in slist:
        if id(e) in seen:
            continue
        seen[id(e)] = None
        olist.append(e)
        tl = gc.get_referents(e)
        if tl:
            _getr(tl, olist, seen)


# The public function.
def get_all_objects():
    """Return a list of all live Python
    objects, not including the list itself."""
    gcl = gc.get_objects()
    olist = []
    seen = dict()
    # Just in case:
    seen[id(gcl)] = None
    seen[id(olist)] = None
    seen[id(seen)] = None
    # _getr does the real work.
    _getr(gcl, olist, seen)
    return olist


if __name__ == "__main__":
    # Should return more values than gc.get_objects()
    print(len(get_all_objects()))
    print(len(gc.get_objects()))

    class Foo:
        def bar(self):
            return f"Foo(id={hex(id(self))})"

    items = [Foo() for _ in range(3)]
    print([o.bar() for o in get_all_objects() if isinstance(o, Foo)])
