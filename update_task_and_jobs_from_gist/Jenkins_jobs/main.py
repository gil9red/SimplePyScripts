#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import re
from bs4 import BeautifulSoup
from common import get_jobs, client


def is_equals_config(config_1: str, config_2: str) -> bool:
    def _to_plain_text(xml: str) -> str:
        xml = BeautifulSoup(xml, "html.parser").get_text(strip=True)
        return re.sub(r"\s", "", xml)

    return _to_plain_text(config_1) == _to_plain_text(config_2)


XML_JOB_TEMPLATE = r"""
<?xml version='1.0' encoding='UTF-8'?>
<project>
  <description><![CDATA[{description}]]></description>
  <triggers>
    <hudson.triggers.TimerTrigger>
      <spec>{cron}</spec>
    </hudson.triggers.TimerTrigger>
  </triggers>
  <builders>
    <hudson.tasks.BatchFile>
      <command><![CDATA[{command}]]></command>
    </hudson.tasks.BatchFile>
  </builders>
</project>
""".strip()

jobs = get_jobs("jenkins.yaml")
for job_name, job_data in jobs.items():
    description = job_data["description"]
    cron = job_data["cron"]
    command = job_data["command"].format(
        root_dir=job_data["root_dir"],
        name=job_name,
    )
    print(f"Обработка задачи {job_name!r}")

    xml = XML_JOB_TEMPLATE.format(
        description=description,
        cron=cron,
        command=command,
    )

    job = client.get_job(job_name)
    if job:
        config = job.configure()
        if is_equals_config(xml, config):
            print("Изменений нет")
        else:
            print("Обновление задачи")
            job.configure(xml)
    else:
        print("Создание задачи")
        client.create_job(job_name, xml)

    print()

jobs_deprecated = get_jobs("jenkins.yaml.deprecated")
for job_name in jobs_deprecated.keys():
    job = client.get_job(job_name)
    if job:
        print(f"Удаление устаревшей задачи {job_name!r}")
        job.delete()
