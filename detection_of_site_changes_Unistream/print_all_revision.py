#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""Скрипт выводит все текстовые ревизии."""


if __name__ == "__main__":
    from main import session, TextRevision

    text_revisions = session.query(TextRevision).all()
    for i, rev in enumerate(text_revisions, 1):
        print(i, rev, len(rev.text))
