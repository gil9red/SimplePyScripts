# coding=utf-8
__author__ = "ipetrash"


import argparse
import sys
import os


def main(namespace) -> None:
    # @param namespace argparse.Namespace Содержит переданные в аргументах объекты.
    indent = " " * 8

    dirs = filter(
        lambda x: os.path.isdir(os.path.join(namespace.dir, x)),
        os.listdir(namespace.dir),
    )
    for dir in dirs:
        print(
            indent
            + """<Note fore_color="#000000" back_color="#ffffff" id="%s"/>""" % dir
        )


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="CreateNoteXml",
        description="Cкрипт генерирует xml-файл программы NotesManager.",
        epilog="(с) Petrash Ilya 2014. Автор: Илья Петраш.",
    )
    parser.add_argument("-dir", help="Путь к директории notes.", type=str)
    return parser


if __name__ == "__main__":
    parser = create_parser()

    # TODO: Remove
    # sys.argv = [
    #     sys.argv[0],
    #     r"-dir=C:\Users\ipetrash\Desktop\NotesManager.v0.0.3.Windows\notes",
    # ]

    if len(sys.argv) == 1:
        parser.print_help()
    else:
        namespace = parser.parse_args()
        main(namespace)
