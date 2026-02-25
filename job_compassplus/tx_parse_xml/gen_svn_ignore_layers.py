#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import fnmatch
from pathlib import Path


def process(path: Path, include: str, excludes: list[str], encoding: str = "utf-8"):
    path_exclude: Path = path / "additional_layers_exclude.bat"
    path_restore: Path = path / "additional_layers_restore_exclude.bat"

    print(f"Writing to file {path_exclude}")
    print(f"Writing to file {path_restore}")

    with (
        open(path_exclude, "w", encoding=encoding) as f_exclude,
        open(path_restore, "w", encoding=encoding) as f_restore,
    ):
        for p in path.glob(include):
            if not p.is_dir():
                continue

            dir_name: str = p.name

            is_exclude: bool = any(
                True for pattern in excludes if fnmatch.fnmatch(dir_name, pattern)
            )
            if is_exclude:
                f_exclude.write("REM ")  # NOTE: Комментарий для Windows
            f_exclude.write(f"svn update --set-depth exclude {dir_name}\n")

            f_restore.write(f"svn update --set-depth infinity {dir_name}\n")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Generating batch files to exclude additional layers folders",
    )
    parser.add_argument(
        "path",
        metavar="/PATH/TO/PROJECT",
        type=Path,
        help="Path to project (the directory containing branch.xml)",
    )
    parser.add_argument(
        "--include",
        type=str,
        default="com.tranzaxis.*",
        help="Glob for include folders (default: %(default)s)",
    )
    parser.add_argument(
        "--excludes",
        nargs="+",
        type=str,
        default=["com.tranzaxis.experimental", "com.tranzaxis.demo"],
        help="Globs for exclude folders (default: %(default)s)",
    )
    args = parser.parse_args()

    process(args.path, args.include, args.excludes)
