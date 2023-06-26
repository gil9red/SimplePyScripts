#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from show_maintainers import get_owner_by_modules


project_dir = "C:/DEV__TX/trunk_tx"

with open("maintainers.txt", "w", encoding="utf-8") as f:
    owner_by_modules = get_owner_by_modules(project_dir)

    lines = []
    for email in sorted(owner_by_modules):
        modules = owner_by_modules[email]
        modules.sort()

        lines.append(f"{email} ({len(modules)}):")
        for module in modules:
            lines.append(f"    {module}")
        lines.append("")

    text = "\n".join(lines).strip()
    f.write(text)
