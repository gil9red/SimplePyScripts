#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://docs.python.org/3/library/secrets.html#secrets.token_urlsafe


from secrets import token_urlsafe


if __name__ == "__main__":
    # Example:
    url = "https://mydomain.com/reset=" + token_urlsafe()
    print(url)
    print()

    for i in (None, 8, 8, 16, 32):
        token = token_urlsafe() if i is None else token_urlsafe(i)
        print(f"[{len(token)}]: {token}")
