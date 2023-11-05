#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from common import get_jobs_for_run, client


def run_job(job):
    print(f"Run {job.full_name!r}")
    job.build()


def run_in_view(view_name: str):
    for job in client.views.get(view_name):
        run_job(job)


for job_name in get_jobs_for_run().keys():
    job = client.get_job(job_name)
    run_job(job)
