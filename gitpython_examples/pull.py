#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


if __name__ == "__main__":
    from common import get_repo

    repo = get_repo()
    repo.remotes.origin.pull()
