#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import re


print(f"My cool string is called {__author__}.")
print()

name = __author__
print(f"My cool string is called {name}.")
print(f"My cool string is called {name.upper()}.")
print(
    f"My cool string is called {''.join(c.lower() if i % 2 else c.upper() for i, c in enumerate(__author__))}."
)
print(f"My cool string is called {name.replace('etr', '123')}.")
print()

print()
a = 1
f = f"{a + 1}"
print(f"fff{f + f'{f}' + f'{a}'}")  # fff221
print()


def strange_1(text):
    return "".join(c.lower() if i % 2 else c.upper() for i, c in enumerate(text))


print("Use function:")
print(f"My cool string is called {strange_1(name)}.")
print()

print("Use regexp:")
print(f"My cool string is called {re.sub(r'[a, e]', '0', name)}.")
print()


# Use class
class Foo:
    def __init__(self, text="") -> None:
        self.text = text

    def strange_2(self, text):
        return re.sub(r"[aeo]", " ", text)

    @staticmethod
    def strange_3(text) -> str:
        return f'"{text}"'

    def __format__(self, format_spec) -> str:
        format_spec = format_spec.strip()

        if not format_spec:
            return self.__str__()

        if format_spec == "upper :)":
            return self.__str__().upper()

        if format_spec == "revert":
            return self.__str__()[::-1]

        return self.__str__()

    def __str__(self) -> str:
        return f'<Foo(text="{self.text}")>'

    def __repr__(self) -> str:
        return f'<Foo(text="{self.text}, id={hex(id(self))}")>'


print("Use class:")
print(f"My cool string is called {Foo().strange_2(name)}.")
print(f"My cool string is called {Foo.strange_3(name)}.")
f = Foo(name)
print(f"My cool string is called {f}.")
print(f"My cool string is called {repr(f)}.")
print(f"My cool string is called {f!r}.")
print()

print("Use class __format__:")
print(f"My cool string is called {f:upper :)}.")
print(f"My cool string is called {f:    upper :)}.")
print(f"My cool string is called {f:revert}.")
print()

print("Loop:")
for i in range(1, 10):
    print(f"  {i}: {i * i}")

print()

print("Lambda:")
print(f"My cool string is called {(lambda x: x.upper())(name)}.")
print()

print(
    "Raw and f-strings may be combined. For example, they could be used to build up regular expressions:"
)
header = "Subject"
print(rf"{header}:\s+")
