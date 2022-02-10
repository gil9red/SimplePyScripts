#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# SOURCE: https://docs.microsoft.com/en-us/windows/win32/taskschd/taskschedulerschema-task-element
# SOURCE: https://docs.microsoft.com/en-us/windows/win32/taskschd/execaction
# SOURCE: https://docs.microsoft.com/en-us/windows/win32/taskschd/comhandleraction
# SOURCE: https://docs.microsoft.com/en-us/windows/win32/taskschd/emailaction
# SOURCE: https://docs.microsoft.com/en-us/windows/win32/taskschd/showmessageaction


import datetime as DT
import enum
from dataclasses import dataclass, field
from typing import List, TypeVar

# pip install pywin32
import pywintypes
import win32com.client


# SOURCE: https://docs.microsoft.com/en-us/windows/win32/api/taskschd/nf-taskschd-itaskfolder-gettasks#parameters
#         Specifies whether to retrieve hidden tasks. Pass in TASK_ENUM_HIDDEN to retrieve all tasks in the folder
#         including hidden tasks, and pass in 0 to retrieve all the tasks in the folder excluding the hidden tasks.
TASK_ENUM_HIDDEN = 1


class TaskStateEnum(enum.IntEnum):
    Unknown = 0
    Disabled = enum.auto()
    Queued = enum.auto()
    Ready = enum.auto()
    Running = enum.auto()


# https://docs.microsoft.com/en-us/windows/win32/taskschd/action-type
class TaskActionEnum(enum.IntEnum):
    Exec = 0
    ComHandler = 5
    SendEmail = 6
    ShowMessage = 7


@dataclass
class ExecAction:
    path: str
    working_directory: str
    arguments: str

    @classmethod
    def get_from(cls, action: win32com.client.CDispatch) -> 'ExecAction':
        return cls(
            path=action.Path,
            working_directory=action.WorkingDirectory,
            arguments=action.Arguments,
        )


@dataclass
class ComHandlerAction:
    class_id: str
    data: str

    @classmethod
    def get_from(cls, action: win32com.client.CDispatch) -> 'ComHandlerAction':
        return cls(
            class_id=action.ClassId,
            data=action.Data,
        )


@dataclass
class EmailAction:
    from_: str
    to: str
    subject: str
    body: str
    server: str
    # attachments: ???  # TODO: Unknown
    bcc: str
    cc: str
    # header_fields: ???  # TODO: Unknown
    reply_to: str

    @classmethod
    def get_from(cls, action: win32com.client.CDispatch) -> 'EmailAction':
        return cls(
            from_=action.From,
            to=action.To,
            subject=action.Subject,
            body=action.Body,
            server=action.Server,
            # attachments=???  # TODO: Unknown
            bcc=action.Bcc,
            cc=action.Cc,
            # header_fields=xxx,  # TODO: Unknown
            reply_to=action.ReplyTo,
        )


@dataclass
class ShowMessageAction:
    title: str
    message_body: str

    @classmethod
    def get_from(cls, action: win32com.client.CDispatch) -> 'ShowMessageAction':
        return cls(
            title=action.Title,
            message_body=action.MessageBody,
        )


ActionType = TypeVar('ActionType', ExecAction, ComHandlerAction, EmailAction, ShowMessageAction)


@dataclass
class Task:
    name: str
    path: str
    hidden: bool
    state: str
    enabled: bool
    last_run_time: DT.datetime
    last_task_result: int
    next_run_time: DT.datetime
    number_of_missed_runs: int
    actions: List[ActionType] = field(default_factory=list)

    @classmethod
    def get_from(cls, task: win32com.client.CDispatch) -> 'Task':
        try:
            hidden = task.Definition.Settings.Hidden
        except pywintypes.com_error:
            hidden = False

        try:
            def_actions = task.Definition.Actions
        except pywintypes.com_error:
            def_actions = []
        actions = []

        for action_com_obj in def_actions:
            action_type = TaskActionEnum(action_com_obj.Type)

            if action_type == TaskActionEnum.Exec:
                actions.append(ExecAction.get_from(action_com_obj))
            elif action_type == TaskActionEnum.ComHandler:
                actions.append(ComHandlerAction.get_from(action_com_obj))
            elif action_type == TaskActionEnum.SendEmail:
                actions.append(EmailAction.get_from(action_com_obj))
            elif action_type == TaskActionEnum.ShowMessage:
                actions.append(ShowMessageAction.get_from(action_com_obj))

        return cls(
            name=task.Name,
            path=task.Path,
            hidden=hidden,
            state=TaskStateEnum(task.State).name,
            enabled=task.Enabled,
            last_run_time=task.LastRunTime,
            last_task_result=task.LastTaskResult,
            next_run_time=task.NextRunTime,
            number_of_missed_runs=task.NumberOfMissedRuns,
            actions=actions,
        )


def get_tasks() -> List[Task]:
    items = []

    scheduler = win32com.client.Dispatch('Schedule.Service')
    scheduler.Connect()

    folders = [scheduler.GetFolder('\\')]
    while folders:
        folder = folders.pop(0)
        folders += list(folder.GetFolders(0))
        for task_com_obj in folder.GetTasks(TASK_ENUM_HIDDEN):
            items.append(
                Task.get_from(task_com_obj)
            )

    return items


if __name__ == '__main__':
    items = get_tasks()
    print(f'Total task: {len(items)}')

    hidden_tasks = [task for task in items if task.hidden]
    print(f'Total hidden tasks: {len(hidden_tasks)}')

    enabled_tasks = [task for task in items if task.enabled]
    print(f'Total enabled tasks: {len(enabled_tasks)}')

    hidden_and_enabled_tasks = [task for task in items if task.hidden and task.enabled]
    print(f'Total hidden and enabled tasks: {len(hidden_and_enabled_tasks)}')

    print()

    print('First 10 tasks:')
    for i, task in enumerate(items[:10], 1):
        print(f'    {i}. {task}')
