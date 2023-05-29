#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import os

# pip install humanize
from humanize import naturalsize as sizeof_fmt


def progress(count, block_size, total_size):
    percent = count * block_size * 100.0 / total_size
    print(
        f"Download: {sizeof_fmt(count * block_size)}/{sizeof_fmt(total_size)}({percent:.1f}%)"
        + " " * 20,
        end="\r",
    )


def create_test_file():
    file_name = "uploads/bigfile"
    if os.path.exists(file_name):
        return

    # Создание больших файлов для теста
    with open(file_name, "wb") as f:
        for i in range(1024 * 1024 * 600):
            f.write(b"0")


if __name__ == "__main__":
    create_test_file()

    from urllib.request import urlretrieve
    urlretrieve("http://127.0.0.1:5000/files/bigfile", "file", reporthook=progress)
