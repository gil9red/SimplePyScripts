#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from pathlib import Path
import subprocess
from typing import Union


def explore(path: Union[str, Path], select=True):
    path = Path(path).resolve()

    if path.is_dir() or path.is_file():
        args = ["explorer"]
        if select:
            args.append('/select,')
        args.append(str(path))

        subprocess.run(args, shell=True)


if __name__ == '__main__':
    current_dir = Path(__file__).resolve().parent

    # Open parent dir and select <current_dir>
    explore(current_dir)

    # Open <current_dir>
    explore(current_dir, select=False)

    # Open parent dir and select <__file__>
    explore(Path(__file__).resolve())
