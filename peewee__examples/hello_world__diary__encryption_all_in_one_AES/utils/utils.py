#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


def shorten(text: str, width: int = 50) -> str:
    if len(text) <= width:
        return text

    placeholder = "..."
    return text[: width - len(placeholder)] + placeholder
