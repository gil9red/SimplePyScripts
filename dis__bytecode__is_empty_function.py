#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import dis


# https://ru.stackoverflow.com/a/767523/201445
def check_is_empty_function(function):
    instructions = dis.get_instructions(function)
    instr = next(instructions, None)
    if instr is None or instr.opname != "LOAD_CONST" or instr.argrepr != "None":
        return False

    instr = next(instructions, None)
    return instr and (instr.opname == "RETURN_VALUE")


if __name__ == "__main__":

    def foo() -> None:
        pass

    def foo2() -> int:
        return 1

    print("Empty:", check_is_empty_function(foo))
    print("Empty:", check_is_empty_function(foo2))
