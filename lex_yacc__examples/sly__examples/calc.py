#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# SOURCE: https://github.com/dabeaz/sly/
# SOURCE: https://sly.readthedocs.io/en/latest/sly.html


# pip install sly
from sly import Lexer, Parser


class CalcLexer(Lexer):
    tokens = {NAME, NUMBER, PLUS, TIMES, MINUS, DIVIDE, ASSIGN, LPAREN, RPAREN}
    ignore = ' \t'

    # Tokens
    NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'
    NUMBER = r'\d+'

    # Special symbols
    PLUS = r'\+'
    MINUS = r'-'
    TIMES = r'\*'
    DIVIDE = r'/'
    ASSIGN = r'='
    LPAREN = r'\('
    RPAREN = r'\)'

    # Ignored pattern
    ignore_newline = r'\n+'

    # Extra action for newlines
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')

    def error(self, t):
        print(f"Illegal character '{t.value[0]}'")
        self.index += 1


class CalcParser(Parser):
    tokens = CalcLexer.tokens

    precedence = (
        ('left', PLUS, MINUS),
        ('left', TIMES, DIVIDE),
        ('right', UMINUS),
    )

    def __init__(self):
        self.names = dict()

    @_('NAME ASSIGN expr')
    def statement(self, p):
        self.names[p.NAME] = p.expr

    @_('expr')
    def statement(self, p) -> int:
        return p.expr

    @_('expr PLUS expr')
    def expr(self, p):
        return p.expr0 + p.expr1

    @_('expr MINUS expr')
    def expr(self, p):
        return p.expr0 - p.expr1

    @_('expr TIMES expr')
    def expr(self, p):
        return p.expr0 * p.expr1

    @_('expr DIVIDE expr')
    def expr(self, p):
        return p.expr0 / p.expr1

    @_('MINUS expr %prec UMINUS')
    def expr(self, p):
        return -p.expr

    @_('LPAREN expr RPAREN')
    def expr(self, p):
        return p.expr

    @_('NUMBER')
    def expr(self, p) -> int:
        return int(p.NUMBER)

    @_('NAME')
    def expr(self, p):
        try:
            return self.names[p.NAME]
        except LookupError:
            print(f'Undefined name {p.NAME!r}')
            return 0


if __name__ == '__main__':
    lexer = CalcLexer()
    parser = CalcParser()

    text = '2 + 2 * 2'
    value = parser.parse(lexer.tokenize(text))
    print(f'{text} = {value}')
    # 2 + 2 * 2 = 6

    print()

    items = [
        'a = 2',
        'a = a * 2',
        'b = 2',
        'a + b + 1',
    ]
    for line in items:
        value = parser.parse(lexer.tokenize(line))
        if value is not None:
            print(f'{line!r} = {value}')
        else:
            print(f'{line!r}')
    """
    'a = 2'
    'a = a * 2'
    'b = 2'
    'a + b + 1' = 7
    """

    print()

    while True:
        try:
            text = input('calc > ')
        except EOFError:
            break
        if text:
            value = parser.parse(lexer.tokenize(text))
            if value is not None:
                print(value)
