#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from functools import partial
from combine_decorators__with_args import custom_tag


@custom_tag(
    name="a",
    href="https://example.com",
    title="Hint!",
)
def hello(text):
    return text


custom_tag_a = partial(
    custom_tag,
    name="a",
    href="https://example.com",
    title="Hint!",
)


@custom_tag_a()
def hello2(text):
    return text


@custom_tag_a(
    title="Other hint!",
)
def hello3(text):
    return text


print(hello("Foo"))
# <a href="https://example.com" title="Hint!">Foo</a>

print(hello2("Foo"))
# <a href="https://example.com" title="Hint!">Foo</a>

print(hello3("Foo"))
# <a href="https://example.com" title="Other hint!">Foo</a>
