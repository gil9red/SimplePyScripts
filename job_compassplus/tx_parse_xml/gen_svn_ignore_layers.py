#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import fnmatch
import argparse

from pathlib import Path


def process(
    root_path: Path,
    include_glob: str,
    exclude_patterns: list[str],
    encoding: str = "utf-8",
):
    file_exclude: Path = root_path / "svn_layers_exclude.bat"
    file_restore: Path = root_path / "svn_layers_restore.bat"

    print(f"Scanning directory: {root_path.absolute()}")

    target_dirs: list[Path] = [p for p in root_path.glob(include_glob) if p.is_dir()]
    if not target_dirs:
        print("No matching directories found.")
        return

    # Подготавливаем списки строк для записи
    lines_exclude: list[str] = ["@echo off"]
    lines_restore: list[str] = ["@echo off"]

    for p in target_dirs:
        dir_name: str = p.name
        is_excluded: bool = any(
            fnmatch.fnmatch(dir_name, pat) for pat in exclude_patterns
        )

        prefix: str = "REM " if is_excluded else ""
        lines_exclude.append(f"{prefix}svn update --set-depth exclude {dir_name}")
        lines_restore.append(f"{prefix}svn update --set-depth infinity {dir_name}")

    file_exclude.write_text("\n".join(lines_exclude) + "\n", encoding=encoding)
    file_restore.write_text("\n".join(lines_restore) + "\n", encoding=encoding)

    print(f"Done! Created '{file_exclude.name}' and '{file_restore.name}'")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generates SVN batch scripts to manage folder depth (exclude/include).",
    )
    parser.add_argument(
        "path",
        metavar="PROJECT_PATH",
        type=Path,
        help="Path to the project directory",
    )
    parser.add_argument(
        "--include",
        default="com.tranzaxis.*",
        help="Glob pattern for directories to process (default: %(default)s)",
    )
    parser.add_argument(
        "--excludes",
        nargs="+",
        default=["com.tranzaxis.experimental", "com.tranzaxis.demo"],
        help="Globs for directories to comment out in exclude script (default: %(default)s)",
    )

    args = parser.parse_args()

    if not args.path.exists():
        parser.error(f"The path {args.path} does not exist.")

    process(args.path, args.include, args.excludes)
