#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import re
from pathlib import Path


PATTERN_ID: re.Pattern = re.compile(rb'\bId="([a-zA-Z]{3}\w+)"')


def process(path_layer: Path, path_extract: Path):
    if not path_layer.exists():
        raise Exception(f"Not exists: {path_layer}")

    items: set[bytes] = set()
    for f in path_layer.rglob("*.xml"):
        # TODO: Добавить статистику: файлы, количество найденных
        ids: list[bytes] = PATTERN_ID.findall(f.read_bytes())
        print(f"{f} ids: {len(ids)}")
        items.update(ids)

    with open(path_extract, "wb") as f:
        for value in items:
            f.write(value + b"\n")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Exporting IDs to a file"
    )
    parser.add_argument(
        "path_layer",
        metavar="/PATH/TO/TRUNK/LAYER",
        help="Path to layer (the directory containing layer.xml)",
        type=Path,
    )
    parser.add_argument(
        "path_extract",
        help="Path to extract",
        type=Path,
    )
    args = parser.parse_args()

    process(args.path_layer, args.path_extract)
