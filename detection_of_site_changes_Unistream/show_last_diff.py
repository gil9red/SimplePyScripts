#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""Скрипт находит последние две ревизии, сохраняет их текст в файлы и сравнивает с помощью kdiff3."""


if __name__ == "__main__":
    import os
    from main import session, TextRevision

    # TODO: нет смысла запрашивать все, если нужны только 2 последнии
    text_revisions = session.query(TextRevision).all()
    if len(text_revisions) >= 2:
        file_a, file_b = text_revisions[-2:]

        file_name_a = "file_a"
        file_name_b = "file_b"

        with open(file_name_a, mode="w", encoding="utf-8") as f:
            f.write(file_a.text)

        with open(file_name_b, mode="w", encoding="utf-8") as f:
            f.write(file_b.text)

        os.system("kdiff3 {} {}".format(file_name_a, file_name_b))

        if os.path.exists(file_name_a):
            os.remove(file_name_a)

        if os.path.exists(file_name_b):
            os.remove(file_name_b)
