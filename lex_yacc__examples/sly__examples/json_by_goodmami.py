#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://github.com/goodmami/python-parsing-benchmarks/blob/611cfc20ca7b61f1f489b0e56f201f6888a5c67b/bench/helpers.py


"""
JSON parser implemented with SLY

Implemented by Michael Wayne Goodman. For license information, see
https://github.com/goodmami/python-parsing-benchmarks/

"""


import re
from sly import Lexer, Parser


_json_unesc_re = re.compile(r'\\(["/\\bfnrt]|u[0-9A-Fa-f])')
_json_unesc_map = {
    '"': '"',
    "/": "/",
    "\\": "\\",
    "b": "\b",
    "f": "\f",
    "n": "\n",
    "r": "\r",
    "t": "\t",
}


def _json_unescape(m):
    c = m.group(1)
    if c[0] == "u":
        return chr(int(c[1:], 16))
    c2 = _json_unesc_map.get(c)
    if not c2:
        raise ValueError(f"invalid escape sequence: {m.group(0)}")
    return c2


def json_unescape(s):
    return _json_unesc_re.sub(_json_unescape, s[1:-1])


def compile():
    class JsonLexer(Lexer):
        tokens = {STRING, NUMBER, TRUE, FALSE, NULL}
        ignore = " \t\n\r"
        literals = {"{", "}", "[", "]", ":", ","}

        @_(r"-?(0|[1-9][0-9]*)(\.[0-9]+)?([Ee][+-]?[0-9]+)?")
        def NUMBER(self, t):
            try:
                t.value = int(t.value)
            except ValueError:
                t.value = float(t.value)
            return t

        @_(r'"([ !#-\[\]-\U0010ffff]+|\\(["\/\\bfnrt]|u[0-9A-Fa-f]{4}))*"')
        def STRING(self, t):
            t.value = json_unescape(t.value)
            return t

        @_(r"true")
        def TRUE(self, t):
            t.value = True
            return t

        @_(r"false")
        def FALSE(self, t):
            t.value = False
            return t

        @_(r"null")
        def NULL(self, t):
            t.value = None
            return t

    class JsonParser(Parser):
        tokens = JsonLexer.tokens
        start = "value"

        @_(r'"{" [ pairs ] "}"')
        def value(self, p):
            if p.pairs:
                return dict(p.pairs)
            else:
                return {}

        @_(r'pair { "," pair }')
        def pairs(self, p):
            return [p.pair0] + p.pair1

        @_(r'STRING ":" value')
        def pair(self, p):
            return (p.STRING, p.value)

        @_(r'"[" [ items ] "]"')
        def value(self, p):
            if p.items:
                return p.items
            else:
                return []

        @_(r'value { "," value }')
        def items(self, p):
            return [p.value0] + p.value1

        @_("STRING", "NUMBER", "TRUE", "FALSE", "NULL")
        def value(self, p):
            return p[0]

        def error(self, p):
            raise ValueError(p)

    lexer = JsonLexer()
    parser = JsonParser()

    return lambda s: parser.parse(lexer.tokenize(s))


parse = compile()


if __name__ == "__main__":
    text = '{"abc": [1, 2.5, 3.0, true, null], "value": "123"}'

    print(parse(text))
    # {'abc': [1, 2.5, 3.0, True, None], 'value': '123'}

    import json
    print(json.loads(text))
    # {'abc': [1, 2.5, 3.0, True, None], 'value': '123'}
