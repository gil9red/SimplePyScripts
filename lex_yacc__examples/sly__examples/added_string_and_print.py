#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://github.com/dabeaz/sly/
# SOURCE: https://sly.readthedocs.io/en/latest/sly.html


# pip install sly
from sly import Lexer, Parser


class MyLexer(Lexer):
    tokens = {
        NAME,
        TEXT,
        NUMBER,
        PRINT,
        PLUS,
        TIMES,
        MINUS,
        DIVIDE,
        ASSIGN,
        LPAREN,
        RPAREN,
    }
    ignore = " \t"

    # Tokens
    NUMBER = r"\d+"
    NAME = r"[a-zA-Z_][a-zA-Z0-9_]*"
    NAME["print"] = PRINT

    @_(r'".+?"', r"'.+?'")
    def TEXT(self, t):
        return t

    # Special symbols
    PLUS = r"\+"
    MINUS = r"-"
    TIMES = r"\*"
    DIVIDE = r"/"
    ASSIGN = r"="
    LPAREN = r"\("
    RPAREN = r"\)"

    # Ignored pattern
    ignore_newline = r"\n+"

    # Extra action for newlines
    def ignore_newline(self, t) -> None:
        self.lineno += t.value.count("\n")

    def error(self, t) -> None:
        print(f"Illegal character '{t.value[0]}'")
        self.index += 1


class MyParser(Parser):
    tokens = MyLexer.tokens

    precedence = (
        ("left", PLUS, MINUS),
        ("left", TIMES, DIVIDE),
        ("right", UMINUS),
    )

    def __init__(self) -> None:
        self.names = dict()

    @_("NAME ASSIGN expr")
    def statement(self, p) -> None:
        self.names[p.NAME] = p.expr

    @_("expr")
    def statement(self, p) -> int | str:
        return p.expr

    @_("PRINT expr")
    def statement(self, p) -> None:
        print(p.expr)

    @_("expr PLUS expr")
    def expr(self, p):
        # Javascript style :D
        if isinstance(p.expr0, str) or isinstance(p.expr1, str):
            return str(p.expr0) + str(p.expr1)

        return p.expr0 + p.expr1

    @_("expr MINUS expr")
    def expr(self, p):
        return p.expr0 - p.expr1

    @_("expr TIMES expr")
    def expr(self, p):
        return p.expr0 * p.expr1

    @_("expr DIVIDE expr")
    def expr(self, p):
        return p.expr0 / p.expr1

    @_("MINUS expr %prec UMINUS")
    def expr(self, p):
        return -p.expr

    @_("LPAREN expr RPAREN")
    def expr(self, p):
        return p.expr

    @_("NUMBER")
    def expr(self, p) -> int:
        return int(p.NUMBER)

    @_("TEXT")
    def expr(self, p) -> str:
        return p.TEXT[1:-1]

    @_("NAME")
    def expr(self, p):
        try:
            return self.names[p.NAME]
        except LookupError:
            print(f"Undefined name {p.NAME!r}")
            return 0


if __name__ == "__main__":
    lexer = MyLexer()
    parser = MyParser()

    text = """
    "12" + '3' + 456
    """.strip()
    value = parser.parse(lexer.tokenize(text))
    print(f"{text} = {value!r}")
    # 12 + '3' + 456 = '123456'

    print()

    text = """
    "12" + '3'
    """.strip()
    value = parser.parse(lexer.tokenize(text))
    print(f"{text} = {value!r}")
    # "12" + '3' = '123'

    print()

    items = [
        """text = "Hello " + 'World!'""",
        "text",
    ]
    for line in items:
        value = parser.parse(lexer.tokenize(line))
        if value is not None:
            print(f"{line} = {value!r}")
        else:
            print(line)
    # text = "Hello " + 'World!'
    # text = 'Hello World!'

    print()

    for line in [
        'print text + "!!"',
        'print(text + "!!")',
    ]:
        parser.parse(lexer.tokenize(line))

    print()

    while True:
        try:
            text = input("calc > ")
        except EOFError:
            break
        if text:
            value = parser.parse(lexer.tokenize(text))
            if value is not None:
                print(value)
