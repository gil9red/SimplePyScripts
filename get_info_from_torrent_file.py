#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import re


def tokenize(text, match=re.compile("([idel])|(\d+):|(-?\d+)").match):
    i = 0
    while i < len(text):
        m = match(text, i)
        s = m.group(m.lastindex)
        i = m.end()
        if m.lastindex == 2:
            yield "s"
            yield text[i:i+int(s)]
            i = i + int(s)
        else:
            yield s


def decode_item(next, token):
    if token == "i":
        # integer: "i" value "e"
        data = int(next())
        if next() != "e":
            raise ValueError
    elif token == "s":
        # string: "s" value (virtual tokens)
        data = next()
    elif token == "l" or token == "d":
        # container: "l" (or "d") values "e"
        data = []
        tok = next()
        while tok != "e":
            data.append(decode_item(next, tok))
            tok = next()
        if token == "d":
            data = dict(list(zip(data[0::2], data[1::2])))
    else:
        raise ValueError
    return data


def decode(text):
    try:
        src = tokenize(text)
        data = decode_item(src.__next__, next(src))
        for token in src: # look for more tokens
            raise SyntaxError("trailing junk")
    except (AttributeError, ValueError, StopIteration):
        raise SyntaxError("syntax error")
    return data


if __name__ == '__main__':
    # data = open('[rutor.is]Homeland_Season_06.torrent', "r", encoding='latin1').read()
    import requests
    data = requests.get('http://anti-tor.org/download/544942').content.decode('latin1')
    torrent = decode(data)

    for file in torrent["info"]["files"]:
        print("%r - %d bytes" % ("/".join(file["path"]), file["length"]))
