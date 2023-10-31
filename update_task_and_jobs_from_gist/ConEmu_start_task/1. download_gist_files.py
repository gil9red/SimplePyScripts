#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import re
import sys

from collections import defaultdict
from pathlib import Path

from config import DIR, GIST_URL, DIR_GIST_FILES
from common import (
    PATTERN_FILE_TASK,
    PATTERN_GIST_GROUP,
    fill_string_pattern,
    get_gist_files,
)

sys.path.append(str(DIR.parent))
from root_common import get_gist_file


DEBUG_LOG = False


# Clear directory
for f in get_gist_files():
    f.unlink()

file_text = get_gist_file(GIST_URL, "all.txt")

group: str = ""
group_by_lines = defaultdict(list)
for line in file_text.splitlines():
    if not line:
        continue
    elif line.startswith("# IGNORED"):
        break
    elif m := PATTERN_GIST_GROUP.search(line):
        group = m.group(1)
        if group in group_by_lines:
            raise Exception(f"Duplicate of group = {group!r}")
        continue
    elif line.startswith("#"):
        continue

    DEBUG_LOG and print(line)
    m = re.search(r"[a-z]:[^:]+\.py", line, flags=re.IGNORECASE)
    script_dir_path = Path(m.group()).parent

    if script_dir_path.name.startswith("-"):
        print(f'[#] Do you really need to run "{script_dir_path}"?')
    else:
        assert script_dir_path.exists(), f"{script_dir_path} not exists!"

    line = line.format(
        root_dir=script_dir_path.parent,
        dir=script_dir_path,
        group=group,
    )
    DEBUG_LOG and print(line)

    if not group:
        raise Exception('"# GROUP" must be defined!')

    group_by_lines[group].append(line + "\n")
    DEBUG_LOG and print()

# Save to files
for group, lines in group_by_lines.items():
    file_name = fill_string_pattern(PATTERN_FILE_TASK, group)
    gist_file = DIR_GIST_FILES / file_name
    gist_file.write_text("\n".join(lines), "utf-8")
