#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import subprocess


def get_git_revision_hash() -> str:
    return (
        subprocess
        .check_output(["git", "rev-parse", "HEAD"])
        .strip()
        .decode("utf-8"))


def get_git_revision_short_hash() -> str:
    return (
        subprocess
        .check_output(["git", "rev-parse", "--short", "HEAD"])
        .strip()
        .decode("utf-8")
    )


if __name__ == "__main__":
    print(get_git_revision_hash())
    # c2d959d5e658ef2279e5e79ab21cf6e1f6a71597

    print(get_git_revision_short_hash())
    # c2d959d5
