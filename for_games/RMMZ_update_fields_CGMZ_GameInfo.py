#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import json
import subprocess

import re

from pathlib import Path


PATTERN_FIELD_VERSION: re.Pattern = re.compile(r'(?P<left>"Left Text"\s*:\s*)".+?"')


def process(path_dir: Path, forced: bool = False):
    path_js_plugins: Path = path_dir / "js" / "plugins.js"

    # If the last commit was in path_js_plugins, then skipping the file change
    result: bytes = subprocess.check_output(
        args=["git", "diff", "HEAD~1", "HEAD", path_js_plugins],
        cwd=path_dir,
    )
    if result and not forced:
        print(
            f"Skipping change {path_js_plugins} because the file is in the last commit"
        )
        return

    result: str = subprocess.check_output(
        args=[
            "git",
            "log",
            "-1",
            '--pretty=format:{"hash":"%h","datetime":"%ad"}',
            "--date=format:%Y-%m-%d %H:%M:%S",
        ],
        cwd=path_dir,
        encoding="utf-8",
    )
    print("Git log:", result)

    data: dict[str, str] = json.loads(result)
    print("Git log (parsed):", data)

    version: str = f'v{data["hash"]} ({data["datetime"]})'
    print(f"Version: {version}")

    js_plugins: str = path_js_plugins.read_text(encoding="utf-8")
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

    print(f"Write to {path_js_plugins}")
    path_js_plugins.write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Writes information about the last git commit to the CGMZ_GameInfo plugin parameter."
    )
    parser.add_argument(
        "path_project",
        help="Path to project (the directory containing game.rmmzproject)",
        type=Path,
    )
    parser.add_argument(
        "--forced",
        help="Force update",
        action="store_true",
        default=False,
    )
    args = parser.parse_args()

    process(
        path_dir=args.path_project,
        forced=args.forced,
    )
