#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from pathlib import Path
from collections import Counter, defaultdict

# pip install humanize
from humanize import naturalsize as sizeof_fmt


def process(path_layer: str):
    if isinstance(path_layer, str):
        path_layer = Path(path_layer)

    if not path_layer.exists():
        raise Exception(f"Not exists: {path_layer}")

    total_files: int = 0
    module_by_size = Counter()

    for path_bin in Path(path_layer).glob("ads/*/bin"):
        module: str = path_bin.parent.name
        sizes: list[int] = [f.stat().st_size for f in path_bin.glob("*.jar")]
        if not sizes:
            continue

        total_files += len(sizes)
        module_by_size[module] = sum(sizes)

    print(f"Total modules: {len(module_by_size)}")
    print(f"Total files: {total_files}")
    print("Top10 modules by size:")
    for module, size in module_by_size.most_common(10):
        print(f"    {module}: {sizeof_fmt(size)} ({size} bytes)")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Counting size bin of ADS modules"
    )
    parser.add_argument(
        "path_layer",
        metavar="/PATH/TO/TRUNK/LAYER",
        help="Path to layer (the directory containing layer.xml)",
    )
    args = parser.parse_args()

    process(args.path_layer)
