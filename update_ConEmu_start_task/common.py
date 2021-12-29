#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import re
from pathlib import Path
from typing import List

from config import DIR_GIST_FILES


def get_gist_files() -> List[Path]:
    def _get_number(f: Path) -> int:
        return int(''.join(c for c in f if c.isdigit()))

    return sorted(
        (f for f in DIR_GIST_FILES.glob('*') if f.is_file()),
        key=lambda file_name: _get_number(file_name.stem)
    )


# SOURCE: https://github.com/gil9red/telegram_bot__gamebook/blob/7b7399c83ae6249da9dc92ea5dc475cc0565edc0/bot/regexp.py#L22
def fill_string_pattern(pattern: re.Pattern, *args) -> str:
    pattern = pattern.pattern
    pattern = pattern.strip('^$')
    return re.sub(r'\(.+?\)', '{}', pattern).format(*args)


PATTERN_CONEMU_TASK = re.compile(r'My python (\d+)', flags=re.IGNORECASE)
PATTERN_FILE_TASK = re.compile(r'^group (\d+)$', flags=re.IGNORECASE)


if __name__ == '__main__':
    files = get_gist_files()
    print(f'Files ({len(files)}): {[f.stem for f in files]}')
    print()

    assert fill_string_pattern(PATTERN_FILE_TASK, 123) == 'group 123'
    assert fill_string_pattern(PATTERN_FILE_TASK, 1) == 'group 1'
    assert fill_string_pattern(PATTERN_FILE_TASK, "123 [yt]") == 'group 123 [yt]'

    assert fill_string_pattern(PATTERN_CONEMU_TASK, 123) == 'My python 123'
    assert fill_string_pattern(PATTERN_CONEMU_TASK, 1) == 'My python 1'
    assert fill_string_pattern(PATTERN_CONEMU_TASK, "123 [yt]") == 'My python 123 [yt]'
