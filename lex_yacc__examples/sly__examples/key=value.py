#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# pip install sly
from sly import Lexer, Parser


class MyLexer(Lexer):
    tokens = {NAME, ASSIGN, VALUE}
    ignore = ' \t'

    # Tokens
    NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'
    ASSIGN = '='
    VALUE = r'.+'

    # Ignored pattern
    ignore_newline = r'\n+'

    # Extra action for newlines
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')

    def error(self, t):
        print(f"Illegal character {t.value[0]!r}")
        self.index += 1


class MyParser(Parser):
    tokens = MyLexer.tokens

    def __init__(self):
        self.names = dict()

    @_('NAME ASSIGN VALUE')
    def statement(self, p):
        self.names[p.NAME] = p.VALUE


if __name__ == '__main__':
    lexer = MyLexer()

    text = 'abc=123'
    print(*list(lexer.tokenize(text)), sep='\n')
    """
    Token(type='NAME', value='abc', lineno=1, index=0, end=3)
    Token(type='ASSIGN', value='=', lineno=1, index=3, end=4)
    Token(type='VALUE', value='123', lineno=1, index=4, end=7)
    """
    print()

    parser = MyParser()

    lines = ['abc=123', 'x = 999', 'y = 111']
    for line in lines:
        tokens = lexer.tokenize(line)
        parser.parse(tokens)

    print(parser.names)
    # {'abc': '123', 'x': '999', 'y': '111'}
