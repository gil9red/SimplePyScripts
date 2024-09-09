#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from pathlib import Path


DIR = Path(__file__).resolve().parent

ROOT_DIR = DIR.parent
PATH_FAVICON = DIR / "favicon.png"

USERNAME: str = "ipetrash"
MAX_RESULTS: int = 500

JIRA_HOST: str = "https://helpdesk.compassluxe.com"
