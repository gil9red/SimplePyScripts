#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://stackoverflow.com/a/9558001/5909792


import ast
import operator as op


# Supported operators
OPERATORS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.FloorDiv: op.floordiv,
    ast.Pow: op.pow,
    ast.BitXor: op.xor,
    ast.USub: op.neg,
}


def eval_(node):
    if isinstance(node, ast.Num):  # <number>
        return node.n

    elif isinstance(node, ast.BinOp):  # <left> <operator> <right>
        return OPERATORS[type(node.op)](eval_(node.left), eval_(node.right))

    elif isinstance(node, ast.UnaryOp):  # <operator> <operand> e.g., -1
        return OPERATORS[type(node.op)](eval_(node.operand))

    else:
        raise TypeError(node)


def eval_expr(expr):
    """
    >>> eval_expr('2^6')
    4
    >>> eval_expr('2**6')
    64
    >>> eval_expr('1 + 2*3**(4^5) / (6 + -7)')
    -5.0
    """

    return eval_(ast.parse(expr, mode="eval").body)


if __name__ == "__main__":
    print(eval_expr("2 + 2 * 2"))    # 6
    print(eval_expr("(2 + 2) * 2"))  # 8
    print(eval_expr("10 * 10"))      # 100
    print(eval_expr("100 / 10"))     # 10.0
    print(eval_expr("100 // 10"))    # 10
    print(eval_expr("2 ** 3"))       # 8
