#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# pip install pywin32
from win32com.client import Dispatch


def create_shortcut(file_name: str, target: str, work_dir: str, arguments: str = ''):
    shell = Dispatch('WScript.Shell')
    shortcut = shell.CreateShortCut(file_name)
    shortcut.TargetPath = target
    shortcut.Arguments = arguments
    shortcut.WorkingDirectory = work_dir
    shortcut.save()


if __name__ == '__main__':
    from pathlib import Path

    abs_file_name = r'C:\Program Files (x86)\ConEmu\ConEmu.exe'
    path = Path(abs_file_name)

    name = 'My startup python scripts 1'

    create_shortcut(
        file_name=f"ConEmu start task '{name}'.lnk",
        target=str(path),
        work_dir=str(path.parent),
        arguments='/cmd {%s} -new_console' % name,
    )
    # NOTE: same
    # create_shortcut(
    #     file_name=f"ConEmu start task '{name}'.lnk",
    #     target=r'C:\Program Files (x86)\ConEmu\ConEmu.exe',
    #     work_dir=r"C:\Program Files (x86)\ConEmu",
    #     arguments='/cmd {%s} -new_console' % name,
    # )
