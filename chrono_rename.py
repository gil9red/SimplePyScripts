#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import argparse

from datetime import datetime
from pathlib import Path
from typing import Final

DEFAULT_PATTERN: Final[str] = "{prefix}{datetime_fmt}{postfix}{suffix}"
DEFAULT_PREFIX: Final[str] = ""
DEFAULT_POSTFIX: Final[str] = ""
DEFAULT_DATETIME_FMT: Final[str] = "%Y-%m-%d_%H-%M-%S-%f"


def process(
    dir_path: Path,
    pattern: str = DEFAULT_PATTERN,
    prefix: str = DEFAULT_PREFIX,
    postfix: str = DEFAULT_POSTFIX,
    datetime_fmt: str = DEFAULT_DATETIME_FMT,
) -> None:
    print("Processing parameters:")
    print(f"  Directory: {dir_path}")
    print(f"  Pattern:   {pattern!r}")
    print(f"  Prefix:    {prefix!r}")
    print(f"  Postfix:   {postfix!r}")
    print(f"  Format:    {datetime_fmt!r}")
    print("-" * 40)
    print()

    for path in dir_path.rglob("*.*"):
        if not path.is_file():
            continue

        mtime_timestamp = path.stat().st_mtime
        mtime: datetime = datetime.fromtimestamp(mtime_timestamp)

        new_name: str = pattern.format(
            prefix=prefix,
            datetime_fmt=mtime.strftime(datetime_fmt),
            postfix=postfix,
            suffix=path.suffix,
        )

        new_path: Path = path.parent / new_name
        if path.name == new_path.name:
            continue

        print(f'Renaming "{path}" to "{new_path.name}"')
        path.rename(new_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Rename files based on their modification date and time.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "dir_path",
        type=Path,
        help="Path to the target directory",
    )
    parser.add_argument(
        "--pattern",
        type=str,
        default=DEFAULT_PATTERN,
        help="Filename pattern template",
    )
    parser.add_argument(
        "--prefix",
        type=str,
        default=DEFAULT_PREFIX,
        help="Prefix to add before the date",
    )
    parser.add_argument(
        "--postfix",
        type=str,
        default=DEFAULT_POSTFIX,
        help="Postfix to add after the date",
    )
    parser.add_argument(
        "--fmt",
        dest="datetime_fmt",
        type=str,
        default=DEFAULT_DATETIME_FMT,
        help="Date and time format string",
    )

    args = parser.parse_args()

    process(
        dir_path=args.dir_path,
        pattern=args.pattern,
        prefix=args.prefix,
        postfix=args.postfix,
        datetime_fmt=args.datetime_fmt,
    )
