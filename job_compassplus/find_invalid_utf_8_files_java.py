#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from pathlib import Path


def process(path: str):
    if isinstance(path, str):
        path = Path(path)

    if not path.exists():
        raise Exception(f"Not exists: {path}")

    for file in path.rglob("*.java"):
        try:
            file.read_text("utf-8")
        except UnicodeError as e:
            print(f"{file}, error: {e}")
            for line in file.read_bytes().splitlines():
                try:
                    str(line, "utf-8")
                except UnicodeError:
                    print(f"    Line: {line}")

            print()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Find invalid utf-8 files java"
    )
    parser.add_argument(
        "path",
        metavar="/PATH/TO",
        help="Path to source tree",
    )
    args = parser.parse_args()

    process(args.path)
