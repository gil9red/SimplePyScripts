#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# SOURCE: https://github.com/dabeaz/sly/
# SOURCE: https://sly.readthedocs.io/en/latest/sly.html


from typing import Union

# pip install sly
from sly import Lexer, Parser


class MyLexer(Lexer):
    tokens = {
        NAME, NUMBER, IF, ELSE, TRUE, FALSE,
        PLUS, TIMES, MINUS, DIVIDE, LPAREN, RPAREN,
        ASSIGN, EQ, LT, LE, GT, GE, NE,
        QUESTION, COLON,
    }
    ignore = ' \t'

    # Tokens
    NUMBER = r'\d+'
    NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'
    NAME['if'] = IF
    NAME['else'] = ELSE
    NAME['true'] = TRUE
    NAME['false'] = FALSE

    # Special symbols
    PLUS = r'\+'
    MINUS = r'-'
    TIMES = r'\*'
    DIVIDE = r'/'
    LPAREN = r'\('
    RPAREN = r'\)'

    QUESTION = r'\?'
    COLON = r'\:'

    EQ = r'=='
    ASSIGN = r'='
    LE = r'<='
    LT = r'<'
    GE = r'>='
    GT = r'>'
    NE = r'!='

    @_(r'true')
    def TRUE(self, t):
        t.value = True
        return t

    @_(r'false')
    def FALSE(self, t):
        t.value = False
        return t

    # Ignored pattern
    ignore_newline = r'\n+'

    # Extra action for newlines
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')

    def error(self, t):
        print(f"Illegal character '{t.value[0]}'")
        self.index += 1


# TODO: WARNING: 12 shift/reduce conflicts
class MyParser(Parser):
    tokens = MyLexer.tokens

    precedence = (
        ('left', IF, ELSE),
        ('left', EQ, NE, LT, LE, GT, GE),
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

    # Ternary operator python
    @_('expr IF expr ELSE expr')
    def expr(self, p):
        return p.expr0 if p.expr1 else p.expr2

    # Ternary operator c
    @_('expr QUESTION expr COLON expr')
    def expr(self, p):
        return p.expr1 if p.expr0 else p.expr2

    @_('expr LT expr')
    def expr(self, p) -> bool:
        return p.expr0 < p.expr1

    @_('expr LE expr')
    def expr(self, p) -> bool:
        return p.expr0 <= p.expr1

    @_('expr GT expr')
    def expr(self, p) -> bool:
        return p.expr0 > p.expr1

    @_('expr GE expr')
    def expr(self, p) -> bool:
        return p.expr0 >= p.expr1

    @_('expr EQ expr')
    def expr(self, p) -> bool:
        return p.expr0 == p.expr1

    @_('expr NE expr')
    def expr(self, p) -> bool:
        return p.expr0 != p.expr1

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

    @_('TRUE', 'FALSE')
    def expr(self, p) -> bool:
        return p[0]

    @_('NAME')
    def expr(self, p):
        try:
            return self.names[p.NAME]
        except LookupError:
            print(f'Undefined name {p.NAME!r}')
            return 0


if __name__ == '__main__':
    lexer = MyLexer()
    parser = MyParser()

    items = [
        'value = 2 > 1',
        'value',
        'value = 2 + 1 == 6 / 2',
        'value',
    ]
    for line in items:
        value = parser.parse(lexer.tokenize(line))
        if value is not None:
            print(f'{line} = {value!r}')
        else:
            print(line)
    # value = 2 > 1
    # value = True
    # value = 2 + 1 == 6 / 2
    # value = True

    print()

    items = [
        # Ternary operator python
        '123 if value else 456',
        '1 if true else 0',
        '1 if false else 0',
        'true if 2 + 2 == 4 else false',

        # Ternary operator c
        '2 + 1 == 6 / 2 ? 123 : 456',
        'true ? 1 : 0',
        'false ? 1 : 0',
        'x = true ? 123 : 456',
        'x'
    ]
    for line in items:
        value = parser.parse(lexer.tokenize(line))
        if value is not None:
            print(f'({line}) -> {value!r}')
        else:
            print(line)
    # (123 if value else 456) -> 123
    # (1 if true else 0) -> 1
    # (1 if false else 0) -> 0
    # (true if 2 + 2 == 4 else false) -> True
    # (2 + 1 == 6 / 2 ? 123 : 456) -> 123
    # (true ? 1 : 0) -> 1
    # (false ? 1 : 0) -> 0
    # x = true ? 123 : 456
    # (x) -> 123

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
