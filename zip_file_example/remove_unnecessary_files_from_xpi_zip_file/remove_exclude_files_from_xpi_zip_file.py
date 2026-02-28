#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""
Плагин удаляет из архива указанные в exclude файлы.
xpi файл -- плагин для FireFox, является zip архивом.
"""


import argparse
import os.path

from zipfile import ZipFile


EXCLUDE = ["README.md", "run.bat", "xpi.bat"]


def create_parser():
    parser = argparse.ArgumentParser(
        description="Remove unnecessary files from zip.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("zip_file_name", type=str)
    parser.add_argument("--exclude", nargs="*", default=EXCLUDE)
    parser.add_argument("--add_exclude", action="store_true")

    return parser.parse_args()


def do(zip_file_name, exclude) -> None:
    print("zip_file_name:", zip_file_name)

    print("Delete files:", EXCLUDE)

    # Измененный zip
    out_zip_file_name = "_" + zip_file_name

    print(f"open {zip_file_name} and {out_zip_file_name} zip arhives")
    with ZipFile(zip_file_name, "r") as zin, ZipFile(out_zip_file_name, "w") as zout:
        print(f"start fill {out_zip_file_name} zip arhive")

        for item in zin.infolist():
            buffer = zin.read(item.filename)
            if os.path.basename(item.filename) not in exclude:
                zout.writestr(item, buffer)

        print(f"finish fill {out_zip_file_name} zip arhive")

    # Удаляем оригинальный
    print(f"remove original {zip_file_name} zip file")
    os.remove(zip_file_name)

    # Переименовываем измененный zip в оригинальный
    print(f"rename {out_zip_file_name} zip file as original {zip_file_name}")
    os.rename(out_zip_file_name, zip_file_name)


if __name__ == "__main__":
    args = create_parser()

    exclude = EXCLUDE + args.exclude if args.add_exclude else args.exclude
    do(args.zip_file_name, set(exclude))
