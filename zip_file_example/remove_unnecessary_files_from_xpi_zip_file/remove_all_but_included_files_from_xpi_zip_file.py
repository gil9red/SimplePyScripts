#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""
Плагин удаляет из архива все файлы кроме указанных.
xpi файл -- плагин для FireFox, является zip архивом.
"""


import argparse
import fnmatch
import os.path

from zipfile import ZipFile


INCLUDE = ["data/*", "index.js", "bootstrap.js", "package.json", "install.rdf"]


def create_parser():
    parser = argparse.ArgumentParser(
        description="Remove all but included files from zip.py.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("zip_file_name", type=str)
    parser.add_argument("--include", nargs="*", default=INCLUDE)
    parser.add_argument("--add_include", action="store_true")

    return parser.parse_args()


def do(zip_file_name, include) -> None:
    print("zip_file_name:", zip_file_name)
    print("Include files:", include)

    # Измененный zip
    out_zip_file_name = "_" + zip_file_name

    print(f"open {zip_file_name} and {out_zip_file_name} zip arhives")
    with ZipFile(zip_file_name, "r") as zin, ZipFile(out_zip_file_name, "w") as zout:
        print(f"start fill {out_zip_file_name} zip arhive")

        for item in zin.infolist():
            buffer = zin.read(item.filename)

            if any((fnmatch.fnmatch(item.filename, pattern) for pattern in include)):
                zout.writestr(item, buffer)
            else:
                print("Delete", item.filename)

        print(f"finish fill {out_zip_file_name} zip arhive")

    # Удаляем оригинальный
    print(f"remove original {zip_file_name} zip file")
    os.remove(zip_file_name)

    # Переименовываем измененный zip в оригинальный
    print(f"rename {out_zip_file_name} zip file as original {zip_file_name}")
    os.rename(out_zip_file_name, zip_file_name)


if __name__ == "__main__":
    args = create_parser()

    include = set(INCLUDE + args.include if args.add_include else args.include)
    do(args.zip_file_name, include)

    # do('@closingduplicatetabs-0.0.2.xpi', INCLUDE)
