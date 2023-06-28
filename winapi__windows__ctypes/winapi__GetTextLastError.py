#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import ctypes

from win32con import (
    FORMAT_MESSAGE_FROM_SYSTEM,
    FORMAT_MESSAGE_ALLOCATE_BUFFER,
    FORMAT_MESSAGE_IGNORE_INSERTS,
)


def GetTextLastError(error_code=None):
    """
    Функция возвращает текстовое описание ошибки.
    Если не передавать код ошибки, будет возвращаться описание ошибки из GetLastError().

    """

    GetLastError = ctypes.windll.kernel32.GetLastError
    FormatMessage = ctypes.windll.kernel32.FormatMessageA
    LocalFree = ctypes.windll.kernel32.LocalFree

    if error_code is None:
        error_code = GetLastError()

    message_buffer = ctypes.c_char_p()
    FormatMessage(
        FORMAT_MESSAGE_FROM_SYSTEM
        | FORMAT_MESSAGE_ALLOCATE_BUFFER
        | FORMAT_MESSAGE_IGNORE_INSERTS,
        None,
        error_code,
        0,
        ctypes.byref(message_buffer),
        0,
        None,
    )

    error_message = message_buffer.value
    LocalFree(message_buffer)

    error_message = error_message.decode("cp1251").strip()
    return f"{error_code} - {error_message}"


if __name__ == "__main__":
    print(GetTextLastError())
    print(GetTextLastError(128))
