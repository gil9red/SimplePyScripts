#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from collections import Counter, defaultdict
from hashlib import sha1
from pathlib import Path


def process(path: Path) -> None:
    files: list[Path] = [
        p
        for p in path.glob("*/ads/*/img/*")
        if p.suffix.lower() in [".svg", ".png", ".img", ".gif", ".jpg"]
    ]

    suffix_by_number = Counter(p.suffix.lower() for p in files)
    print(f"Suffixes ({len(suffix_by_number)}):")
    for suffix, number in suffix_by_number.items():
        print(f"    {suffix}: {number}")

    print()

    duplicated: dict[str, list[Path]] = defaultdict(list)
    for p in files:
        hash_file = sha1(p.read_bytes()).hexdigest()
        duplicated[hash_file].append(p)

    duplicated = {k: v for k, v in duplicated.items() if len(v) > 1}

    print(f"Duplicates ({len(duplicated)}):")
    for hash_file, items in sorted(duplicated.items(), key=lambda x: len(x[1]), reverse=True):
        print(f"    Hash {hash_file} ({len(items)}):")
        for p in items:
            print(f"      {p}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Search in locale"
    )
    parser.add_argument(
        "path_trunk",
        type=Path,
        metavar="/PATH/TO/TRUNK",
        help="Path to TX source tree (the directory containing branch.xml)",
    )
    args = parser.parse_args()

    process(args.path_trunk)
