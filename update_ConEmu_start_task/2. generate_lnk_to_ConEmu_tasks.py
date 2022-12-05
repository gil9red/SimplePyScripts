#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import sys
sys.path.append('..')

from win_create_shortcut_lnk import create_shortcut

from config import DIR_STARTUP, PATH_CONEMU, PREFIX_LINK
from common import PATTERN_FILE_TASK, PATTERN_CONEMU_TASK, fill_string_pattern, get_gist_files


for f in DIR_STARTUP.glob(f'{PREFIX_LINK}*.lnk'):
    f.unlink()

for f in get_gist_files():
    m = PATTERN_FILE_TASK.search(f.stem)
    if not m:
        continue

    name = fill_string_pattern(PATTERN_CONEMU_TASK, m.group(1))
    file_name_lnk = str(DIR_STARTUP / f"{PREFIX_LINK} '{name}'.lnk")
    print(f'Saving to "{file_name_lnk}"')

    create_shortcut(
        file_name=file_name_lnk,
        target=str(PATH_CONEMU),
        work_dir=str(PATH_CONEMU.parent),
        arguments='/cmd {%s} -new_console' % name,
    )
