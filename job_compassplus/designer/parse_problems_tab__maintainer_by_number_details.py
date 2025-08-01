#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from collections import defaultdict
from common import PATH_PROBLEMS_TAB, Problem, parse_text


text = PATH_PROBLEMS_TAB.read_text("utf-8")

# TODO:
filter_by_codes: list[int] = [
    # 127, 137
]
print(f"Filter by codes: {filter_by_codes}")

user_by_number_details: dict[str, list[Problem]] = defaultdict(list)
code_by_number: dict[int, int] = defaultdict(int)

for p in parse_text(text):
    code: int = p.code
    if filter_by_codes and code not in filter_by_codes:
        continue

    code_by_number[code] += 1

    users = p.maintainers.copy()
    if not users:
        users.append("<unknown>")

    user_by_number_details[", ".join(users)].append(p)

print(f"Total users: {len(user_by_number_details)}")
print(f"Stats (codes {len(code_by_number)}, total {sum(code_by_number.values())}):")
for code, number in sorted(code_by_number.items(), key=lambda x: x[1], reverse=True):
    print(f"    Code {code}: {number}")
print()

INDENT_1: str = "    "

for user, all_problems in sorted(
    user_by_number_details.items(),
    key=lambda x: len(x[1]),
    reverse=True,
):
    print(f"{user!r} ({len(all_problems)}):")

    code_by_problems: dict[int, list[Problem]] = defaultdict(list)
    for p in all_problems:
        code_by_problems[p.code].append(p)

    for code, problems in code_by_problems.items():
        print(f"{INDENT_1}Code {code} ({len(problems)}):")

        for p in problems:
            print(f"{INDENT_1 * 2}[{p.severity}] {p.error} at {p.at}")

    print()

"""
Filter by codes: []
Total users: 4
Stats (codes 4, total 10):
    Code 51: 4
    Code 137: 3
    Code 132: 2
    Code 999: 1

'bar' (5):
    Code 137 (1):
        [NOTE] XXX [bar@example.com] [Fix available] at ABC::Common::Foo::Bar
    Code 51 (4):
        [WARNING] The definition 'ABC::Common::Foo:Bar:ownerPid' is XXX (See RADIX-24309, RADIX-17843. Ignore werror.) [Link] [bar@example.com] at ABC::Common::Foo:Model:Bar
        [WARNING] The definition 'ABC::Common::Foo:Bar:ownerPid' is XXX (See RADIX-24309, RADIX-17843. Ignore werror.) [Link] [bar@example.com] at ABC::Common::Foo:Model:Bar
        [WARNING] The definition 'ABC::Common::Foo:Bar:ownerPid' is XXX (See RADIX-24309, RADIX-17843. Ignore werror.) [Link] [bar@example.com] at ABC::Common::Foo:Model:Bar
        [WARNING] The definition 'ABC::Common::Foo:Bar:ownerPid' is XXX (See RADIX-24309, RADIX-17843. Ignore werror.) [Link] [bar@example.com] at ABC::Common::Foo:Model:Bar

'<unknown>' (2):
    Code 132 (2):
        [NOTE] Editor page does not contain property `XXX` from `overridden` base page (See RADIX-23441) [Link] at ABC::FOO::BAR:General
        [NOTE] Editor page does not contain property `XXX` from `overridden` base page (See RADIX-23441) [Link] at ABC::FOO::BAR:General

'foo, bar' (2):
    Code 137 (1):
        [NOTE] XXX [foo@example.com, bar@example.com] [Fix available] at ABC::Common::Foo::Bar
    Code 999 (1):
        [ERROR] XXX [foo@example.com, bar@example.com] at ABC::Common::Foo::Bar

'foo' (1):
    Code 137 (1):
        [NOTE] XXX [foo@example.com] [Fix available] at ABC::Interfacing.Foo::Bar
"""
