#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import win32clipboard


VALUE_BY_FORMAT: dict[int, str] = {
    getattr(win32clipboard, name): name
    for name in dir(win32clipboard)
    if name.startswith("CF_")
}

win32clipboard.OpenClipboard()
try:
    formats: list[int] = []
    last_format = 0
    while True:
        fmt = win32clipboard.EnumClipboardFormats(last_format)
        if not fmt:
            break

        formats.append(fmt)
        last_format = fmt

    for fmt in formats:
        fmt_name = VALUE_BY_FORMAT.get(fmt)
        if not fmt_name:
            fmt_name = win32clipboard.GetClipboardFormatName(fmt)

        data = win32clipboard.GetClipboardData(fmt)
        value = data[:100] if isinstance(data, (str, bytes)) else data

        print(f"{fmt_name} ({fmt}): size {len(data)}: {value}")

finally:
    win32clipboard.CloseClipboard()
