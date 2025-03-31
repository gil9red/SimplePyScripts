#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import re
from bs4 import BeautifulSoup
from common import get_jobs_for_run, get_jobs_for_delete, client


def is_equals_config(config_1: str, config_2: str) -> bool:
    def _to_plain_text(xml: str) -> str:
        soup = BeautifulSoup(xml, "html.parser")
        xml = soup.get_text(strip=True)
        return re.sub(r"\s", "", xml)

    return _to_plain_text(config_1) == _to_plain_text(config_2)


# Example: http://{url}/job/{job_name}/config.xml
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
  <publishers>
    <hudson.plugins.emailext.ExtendedEmailPublisher plugin="email-ext@2.104">
      <recipientList>$DEFAULT_RECIPIENTS</recipientList>
      <configuredTriggers>
        <hudson.plugins.emailext.plugins.trigger.AbortedTrigger>
          <email>
            <subject>$PROJECT_DEFAULT_SUBJECT</subject>
            <body>$PROJECT_DEFAULT_CONTENT</body>
            <recipientProviders>
              <hudson.plugins.emailext.plugins.recipients.ListRecipientProvider/>
            </recipientProviders>
            <attachmentsPattern></attachmentsPattern>
            <attachBuildLog>false</attachBuildLog>
            <compressBuildLog>false</compressBuildLog>
            <replyTo>$PROJECT_DEFAULT_REPLYTO</replyTo>
            <contentType>project</contentType>
          </email>
        </hudson.plugins.emailext.plugins.trigger.AbortedTrigger>
        <hudson.plugins.emailext.plugins.trigger.FailureTrigger>
          <email>
            <subject>$PROJECT_DEFAULT_SUBJECT</subject>
            <body>$PROJECT_DEFAULT_CONTENT</body>
            <recipientProviders>
              <hudson.plugins.emailext.plugins.recipients.ListRecipientProvider/>
            </recipientProviders>
            <attachmentsPattern></attachmentsPattern>
            <attachBuildLog>false</attachBuildLog>
            <compressBuildLog>false</compressBuildLog>
            <replyTo>$PROJECT_DEFAULT_REPLYTO</replyTo>
            <contentType>project</contentType>
          </email>
        </hudson.plugins.emailext.plugins.trigger.FailureTrigger>
      </configuredTriggers>
      <contentType>default</contentType>
      <defaultSubject>$DEFAULT_SUBJECT</defaultSubject>
      <defaultContent>$DEFAULT_CONTENT</defaultContent>
      <attachmentsPattern></attachmentsPattern>
      <presendScript>$DEFAULT_PRESEND_SCRIPT</presendScript>
      <postsendScript>$DEFAULT_POSTSEND_SCRIPT</postsendScript>
      <attachBuildLog>false</attachBuildLog>
      <compressBuildLog>false</compressBuildLog>
      <replyTo>$DEFAULT_REPLYTO</replyTo>
      <from></from>
      <saveOutput>false</saveOutput>
      <disabled>false</disabled>
    </hudson.plugins.emailext.ExtendedEmailPublisher>
  </publishers>
</project>
""".strip()

jobs: dict[str, dict] = get_jobs_for_run()

total: int = len(jobs)
updated: int = 0
created: int = 0
deleted: int = 0
nothing: int = 0

for job_name, job_data in jobs.items():
    description: str = job_data["description"]
    cron: str = job_data["cron"]
    command: str = job_data["command"].format(
        root_dir=job_data["root_dir"],
        name=job_name,
    )
    print(f"Обработка задачи {job_name!r}")

    xml: str = XML_JOB_TEMPLATE.format(
        description=description,
        cron=cron,
        command=command,
    )

    job = client.get_job(job_name)
    if job:
        config = job.configure()
        if is_equals_config(xml, config):
            print("Изменений нет")
            nothing += 1
        else:
            print("Обновление задачи")
            job.configure(xml)
            updated += 1
    else:
        print("Создание задачи")
        client.create_job(job_name, xml)
        created += 1

    print()

jobs_deprecated: dict[str, dict] = get_jobs_for_delete()
for job_name in jobs_deprecated.keys():
    job = client.get_job(job_name)
    if job:
        print(f"Удаление устаревшей задачи {job_name!r}")
        job.delete()
        deleted += 1

print("\n" + "-" * 10 + "\n")

print(f"""
Всего задач: {total}
Обновлено: {updated}
Создано: {created}
Удалено: {deleted}
Без изменений: {nothing}
""".strip())
