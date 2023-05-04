#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""Скрипт удаляет последнюю ревизию."""


if __name__ == "__main__":
    from main import session, TextRevision

    text_revision = session.query(TextRevision).order_by(TextRevision.id.desc()).first()
    print(text_revision)
    session.delete(text_revision)
    session.commit()
