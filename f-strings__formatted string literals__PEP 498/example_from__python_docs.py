#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


#
# SOURCE: https://docs.python.org/3/reference/lexical_analysis.html#formatted-string-literals
#

import decimal
from datetime import datetime


print("# Some examples of formatted string literals:")
name = "Fred"
print(f"He said his name is {name!r}.")
print(f"He said his name is {repr(name)}.")  # repr() is equivalent to !r

width = 10
precision = 4

value = decimal.Decimal("12.34567")
print(f"result: {value:{width}.{precision}}")  # nested fields

today = datetime(year=2017, month=1, day=27)
print(f"{today:%b %d, %Y}")  # using date format specifier

number = 1024
print(f"{number:#0x}")  # using integer format specifier

print()
print(
    "# A consequence of sharing the same syntax as regular string literals is that characters in the replacement "
    "fields must not conflict with the quoting used in the outer formatted string literal:"
)

a = {"x": "abd"}
# print(f"abc {a["x"]} def")    # error: outer string literal ended prematurely
print(f"abc {a['x']} def")  # workaround: use different quoting

# print('# Backslashes are not allowed in format expressions and will raise an error:')
# f"newline: {ord('\n')}"  # raises SyntaxError

print()
print(
    "# To include a value in which a backslash escape is required, create a temporary variable."
)
newline = ord("\n")
print(f"newline: {newline}")

#
# Formatted string literals cannot be used as docstrings, even if they do not include expressions.


def foo() -> None:
    f"Not a docstring"


print(foo.__doc__ is None)
