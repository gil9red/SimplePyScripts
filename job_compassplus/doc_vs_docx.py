#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from pathlib import Path

# pip install python-docx==1.1.0
from docx import Document


PATH_DIR: str = r"C:\DOC\Specifications\Interfaces"


docx_num = 0
doc_num = 0
for f in Path(PATH_DIR).glob("*.doc*"):
    if f.name.startswith("~"):
        continue

    try:
        Document(f)
        ok = True
        docx_num += 1
    except:
        ok = False
        doc_num += 1

    print(f"[{'+' if ok else '-'}]", f)

print()
print("Total:", docx_num + doc_num)
print("Docx:", docx_num)
print("Doc:", doc_num)
