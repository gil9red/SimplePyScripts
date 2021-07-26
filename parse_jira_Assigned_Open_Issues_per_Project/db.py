#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import datetime as DT
import os
import shutil
import sys

from pathlib import Path
from typing import Dict, Optional

from peewee import *

from common import DIR, print_table

# Для импортирования shorten
sys.path.append(str(DIR.parent))
from shorten import shorten

# Absolute file name
DB_FILE_NAME = str(DIR / 'database.sqlite')


def db_create_backup(backup_dir=DIR / 'backup'):
    os.makedirs(backup_dir, exist_ok=True)

    file_name = str(DT.datetime.today().date()) + '.sqlite'
    file_name = os.path.join(backup_dir, file_name)

    shutil.copy(DB_FILE_NAME, file_name)


# Ensure foreign-key constraints are enforced.
db = SqliteDatabase(DB_FILE_NAME, pragmas={'foreign_keys': 1})


class BaseModel(Model):
    class Meta:
        database = db

    def __str__(self):
        fields = []
        for k, field in self._meta.fields.items():
            v = getattr(self, k)

            if isinstance(field, (TextField, CharField)):
                if v:
                    v = repr(shorten(v))

            elif isinstance(field, ForeignKeyField):
                k = f'{k}_id'
                if v:
                    v = v.id

            fields.append(f'{k}={v}')

        return self.__class__.__name__ + '(' + ', '.join(fields) + ')'


class Run(BaseModel):
    date = DateField(default=DT.date.today)

    def get_total_issues(self) -> int:
        return sum(x.value for x in self.issue_numbers)

    def get_project_by_issue_numbers(self) -> Dict[str, int]:
        return {issue.project.name: issue.value for issue in self.issue_numbers}

    def __str__(self):
        return f'{self.__class__.__name__}(id={self.id}, date={self.date}, total_issues={self.get_total_issues()})'


class Project(BaseModel):
    name = TextField()


class IssueNumber(BaseModel):
    value = IntegerField()
    run = ForeignKeyField(Run, backref='issue_numbers')
    project = ForeignKeyField(Project, backref='issue_numbers')


def add(assigned_open_issues_per_project: Dict[str, int]) -> Optional[bool]:
    last_run = Run.select().order_by(Run.id.desc()).get()
    if assigned_open_issues_per_project == last_run.get_project_by_issue_numbers():
        return

    run, created = Run.get_or_create(date=DT.date.today())
    if not created:
        return False

    for project_name, issue_numbers in assigned_open_issues_per_project.items():
        project, _ = Project.get_or_create(name=project_name)

        IssueNumber.create(
            value=issue_numbers,
            run=run,
            project=project
        )

    db_create_backup()

    return True


db.connect()
db.create_tables([Run, Project, IssueNumber])


if __name__ == '__main__':
    projects = [p.name for p in Project.select()]
    print(f"Projects ({len(projects)}): {projects}\n")

    # Print last rows
    for run in Run.select().order_by(Run.id.desc()).limit(5):
        print(run, '\n')
        print_table(run.get_project_by_issue_numbers())

        print('\n' + '-' * 100 + '\n')
