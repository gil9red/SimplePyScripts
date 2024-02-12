#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from pathlib import Path

import docx
from docx.text.run import Run
from docx.text.paragraph import Paragraph, Run


def get_font_name_and_size(doc: docx.Document, p: Paragraph, r: Run) -> tuple[str | None, int | None]:
    def _get_normal_size(size: int | None) -> int | None:
        return size // 12700 if size else None

    try:
        font_name = r.font.name
    except:
        font_name = None

    if not font_name:
        try:
            font_name = r.style.font.name
        except:
            pass

    if not font_name:
        try:
            font_name = p.style.font.name
        except:
            pass

    # TODO:
    if not font_name:
        try:
            font_name = doc.styles["Normal"].font.name
        except:
            pass

    try:
        font_size = _get_normal_size(r.font.size)
    except:
        font_size = None

    if not font_size:
        try:
            font_size = _get_normal_size(r.style.font.size)
        except:
            pass

    if not font_size:
        try:
            font_size = _get_normal_size(p.style.font.size)
        except:
            pass

    # TODO:
    if not font_size:
        try:
            font_size = _get_normal_size(doc.styles["Normal"].font.size)
        except:
            pass

    return font_name, font_size


dir = Path(__file__).parent / "fill_template"
for file_name in dir.glob("*.docx"):
    print(file_name)

    try:
        doc_file = docx.Document(file_name)

        name_and_size = []
        names = []
        sizes = []

        for p in doc_file.paragraphs:
            for r in p.runs:
                name, size = get_font_name_and_size(doc_file, p, r)
                name_and_size.append((name, size))
                names.append(name)
                sizes.append(size)

        from collections import Counter

        for (name, size), number in Counter(name_and_size).most_common():
            print((name, size), number)

    except Exception as e:
        print(e)

    print()
