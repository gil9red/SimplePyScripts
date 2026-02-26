#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import re
from pathlib import Path


def get_layer_version(path: Path) -> str:
    path = path.resolve()

    if not path.is_dir():
        raise Exception(f"Path {str(path)!r} must be directory")

    path = path / "layer.xml"
    if not path.exists():
        raise Exception(f"Path {str(path)!r} is not exists!")

    m = re.search(r'\bReleaseNumber="(.+?)"', path.read_text("utf-8"))
    if not m:
        raise Exception(f'Not found "ReleaseNumber" in path {str(path)!r}!')

    return m.group(1)


def process(path: Path) -> None:
    print(get_layer_version(path))


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Print a layer version"
    )
    parser.add_argument(
        "path",
        metavar="/PATH/TO/LAYER",
        type=Path,
        help="Path to layer (the directory containing layer.xml)",
    )
    args = parser.parse_args()

    process(args.path)
