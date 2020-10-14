#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import os
import sys

from typing import Optional
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))
from human_byte_size import sizeof_fmt


def get_file_name_from_binary(binary_id: str, binary_content_type: str) -> str:
    fmt = os.path.splitext(binary_id)[-1].lower()

    # Если формат файла есть, хорошо
    if fmt in ['.png', '.jpg', '.jpeg']:
        return binary_id

    content_type = binary_content_type.split('/')[-1]
    return binary_id + '.' + {'jpeg': 'jpg', 'png': 'png'}[content_type]


def get_attribute_value_by_local_name(node, attr_name: str) -> Optional[str]:
    for name, value in node.attrs.items():
        # Получаем имя атрибута
        name = name.split(':')[-1]
        if name == attr_name:
            return value

    return
