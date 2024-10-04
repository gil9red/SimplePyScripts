#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import codecs
import html
import re
from urllib.parse import unquote


# SOURCE: html
_charref = re.compile(
    r'&(#[0-9]+;?'
    r'|#[xX][0-9a-fA-F]+;?'
    r'|[^\t\n\f <&#;]{1,32};?)'
)


# SOURCE: https://stackoverflow.com/a/24519338/5909792
ESCAPE_SEQUENCE_RE = re.compile(r'''
    ( \\U........      # 8-digit hex escapes
    | \\u....          # 4-digit hex escapes
    | \\x..            # 2-digit hex escapes
    | \\[0-7]{1,3}     # Octal escapes
    | \\N\{[^}]+\}     # Unicode characters by name
    | \\[\\'"abfnrtv]  # Single-character escapes
    )''', re.UNICODE | re.VERBOSE)


def decode_escapes(text: str) -> str:
    def decode_match(match: re.Match) -> str:
        return codecs.decode(match.group(0), 'unicode-escape')

    return ESCAPE_SEQUENCE_RE.sub(decode_match, text)


def decode_html(text: str) -> str:
    def _unescape(m: re.Match) -> str:
        return html.unescape(m.group())

    text = _charref.sub(_unescape, text)
    return text


def decode(text: str) -> str:
    text = decode_escapes(text)
    text = decode_html(text)
    text = unquote(text)
    return text


if __name__ == '__main__':
    text = decode_html('&#x20AC; &#8364; &euro;')
    assert text == '€ € €'

    text = decode_html('"Hello" "World"!')
    assert text == '"Hello" "World"!'

    text = decode_html('<p>&#x20AC; &#8364; &euro;</p>')
    assert text == '<p>€ € €</p>'

    assert decode_escapes('') == ''
    assert decode_escapes('Hello') == 'Hello'
    assert decode_escapes('Привет!') == 'Привет!'
    assert decode_escapes(r'\n\r\t\b') == '\n\r\t\b'
    assert decode_escapes(r"\U0001F601") == "\U0001F601"
    assert decode_escapes(r"\U0001F601") == "😁"
    assert decode_escapes(r"\x32\x2B\x32=4") == "2+2=4"
    assert decode_escapes(r"\x32\x2b\x32=\x34") == "2+2=4"
    assert decode_escapes(r"\u0032\u002b\u0032=\u0034") == "2+2=4"
    assert decode_escapes(r"\U00000032\U0000002b\U00000032=\U00000034") == "2+2=4"
    assert decode_escapes(r"\62\53\62\75\64") == "2+2=4"
    assert decode_escapes(r"\N{DIGIT TWO}+\N{DIGIT TWO}=\N{DIGIT FOUR}") == "2+2=4"

    assert decode('\u0032&#x20AC;\n&#8364; \x32&euro; \U0001F601') == '2€\n€ 2€ 😁'
    assert decode('&#x20AC; &#8364; &euro;') == '€ € €'
    assert decode('"Hello" "World"!') == '"Hello" "World"!'

    assert decode('%D0%BD%D0%B0%D1%81%D1%82%D0%BE%D0%BB%D1%8C%D0%BD%D1%8B%D0%B5 %D0%B8%D0%B3%D1%80%D1%8B') == 'настольные игры'
    assert decode('%D0%B8 %D0%B3 %D1%80 %D1%8B') == 'и г р ы'
    assert decode('%D0%B8 %D0%B3 %D1%80 %D1%8B \U0001F601') == 'и г р ы 😁'
