#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import json
import subprocess
import re

from pathlib import Path


# TODO: Название что-то про версию из гита
# TODO: Путь брать относительный
# TODO: Мб его положить в папку etc/ в корне проекта?
DIR: Path = Path(r"C:\Users\ipetrash\Documents\RMMZ\Project1")
PATH_JS_PLUGINS: Path = DIR / "js" / "plugins.js"

PATTERN_FIELD_VERSION: re.Pattern = re.compile(r'(?P<left>"Left Text"\s*:\s*)".+?"')


result: str = subprocess.check_output(
    args=[
        "git",
        "log",
        "-1",
        '--pretty=format:{"hash":"%h","datetime":"%ad"}',
        "--date=format:%Y-%m-%d %H:%M:%S",
    ],
    cwd=DIR,
    encoding="utf-8",
)
print("Git log:", result)

data: dict[str, str] = json.loads(result)
print("Git log (parsed):", data)

version: str = f'v{data["hash"]} ({data["datetime"]})'
print(f"Version: {version}")

js_plugins: str = PATH_JS_PLUGINS.read_text(encoding="utf-8")
lines: list[str] = js_plugins.splitlines()
for i, line in enumerate(lines):
    if "CGMZ_GameInfo" not in line:
        continue

    print(f"Found line {line!r}")

    m = PATTERN_FIELD_VERSION.search(line)
    if not m:
        continue

    current_field_version: str = m.group()

    new_field_version: str = PATTERN_FIELD_VERSION.sub(
        rf'\g<left>"{version}"', current_field_version
    )
    print(f"Replace: {current_field_version!r} -> {new_field_version!r}")

    lines[i] = line.replace(current_field_version, new_field_version)

print(f"Write to {PATH_JS_PLUGINS}")
PATH_JS_PLUGINS.write_text("\n".join(lines) + "\n", encoding="utf-8")
