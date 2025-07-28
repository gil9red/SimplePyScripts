#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import re

from dataclasses import dataclass, field
from pathlib import Path


PATTERN: re.Pattern = re.compile(
    r"\* \[(?P<severity>\w+)\] (?P<code>\d+) - (?P<error>[^\n]+)\n\s*at\s*(?P<at>[^\n]+)"
)


PATH_PROBLEMS_TAB: Path = Path(__file__).parent / "problems_tab.txt"


@dataclass
class Problem:
    severity: str
    code: int
    error: str
    at: str
    maintainers: list[str] = field(default_factory=list)


def parse_text(text: str) -> list[Problem]:
    items: list[Problem] = []

    for m in PATTERN.finditer(text):
        maintainers: list[str] = []
        for brackets in re.findall(r"\[(.*?)]", m.group()):
            if "@" in brackets:
                maintainers += [
                    email.split("@")[0]
                    for email in brackets.split(", ")
                ]

        items.append(
            Problem(
                severity=m.group("severity"),
                code=int(m.group("code")),
                error=m.group("error"),
                at=m.group("at"),
                maintainers=maintainers,
            )
        )

    return items


if __name__ == "__main__":
    from pathlib import Path

    text = PATH_PROBLEMS_TAB.read_text("utf-8")
    problems: list[Problem] = parse_text(text)

    print(f"Problems ({len(problems)}):")
    for i, p in enumerate(problems, 1):
        print(f"{i}. {p}")
