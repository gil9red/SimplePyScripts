#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


def sizeof_fmt(num, suffix='B'):
    for unit in ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)


def get_file_name_from_binary(binary_id: str, binary_content_type: str) -> str:
    print(binary_id, binary_content_type)

    import os
    fmt = os.path.splitext(binary_id)[-1].lower()

    # Если формат файла есть, хорошо
    if fmt in ['.png', '.jpg', '.jpeg']:
        return binary_id

    content_type = binary_content_type.split('/')[-1]
    return binary_id + '.' + {'jpeg': 'jpg', 'png': 'png'}[content_type]