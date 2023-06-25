#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# Добавляем файл в архив
import zipfile


with zipfile.ZipFile("out.zip", mode="w", compression=zipfile.ZIP_DEFLATED) as f:
    f.write("file_1.txt")
    f.write("sub_dir/file_1.1.txt", "file_1.1.txt")

    f.write("sub_dir/file_1.1.txt")
    # out.zip/sub_dir/file_1.1.txt

    f.write(
        "sub_dir/file_1.1.txt", "new_sub_dir/file_1.1.txt"
    )
    # out.zip/new_sub_dir/file_1.1.txt
