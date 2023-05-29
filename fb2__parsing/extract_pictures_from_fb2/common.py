#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import os


def get_file_name_from_binary(binary_id: str, binary_content_type: str) -> str:
    fmt = os.path.splitext(binary_id)[-1].lower()

    # Если формат файла есть, хорошо
    if fmt in [".png", ".jpg", ".jpeg"]:
        return binary_id

    content_type = binary_content_type.split("/")[-1]
    return binary_id + "." + {"jpeg": "jpg", "png": "png"}[content_type]
