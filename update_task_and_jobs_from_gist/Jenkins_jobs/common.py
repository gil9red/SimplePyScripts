#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import sys

# pip install PyYAML
import yaml

# pip install api4jenkins
from api4jenkins import Jenkins

from config import DIR, GIST_URL, JENKINS_URL, LOGIN, PASSWORD

sys.path.append(str(DIR.parent))
from root_common import get_gist_file


def get_jobs(name: str) -> dict[str, dict]:
    text = get_gist_file(GIST_URL, name)
    jobs: dict[str, dict] = yaml.safe_load(text)
    return {k: v for k, v in jobs.items() if not k.startswith("__")}


def get_jobs_for_run() -> dict[str, dict]:
    return get_jobs("jenkins.yaml")


def get_jobs_for_delete() -> dict[str, dict]:
    return get_jobs("jenkins.yaml.deprecated")


client = Jenkins(JENKINS_URL, auth=(LOGIN, PASSWORD))
