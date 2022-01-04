#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import win32com.client
import pywintypes


TASK_ENUM_HIDDEN = 1
TASK_STATE = ['Unknown', 'Disabled', 'Queued', 'Ready', 'Running']

# https://docs.microsoft.com/en-us/windows/win32/taskschd/action-type
TASK_ACTION_EXEC = 0
TASK_ACTION_COM_HANDLER = 5
TASK_ACTION_SEND_EMAIL = 6
TASK_ACTION_SHOW_MESSAGE = 7


scheduler = win32com.client.Dispatch('Schedule.Service')
scheduler.Connect()

n = 0
folders = [scheduler.GetFolder('\\')]
while folders:
    folder = folders.pop(0)
    folders += list(folder.GetFolders(0))
    for task in folder.GetTasks(TASK_ENUM_HIDDEN):
        n += 1

        try:
            settings = task.Definition.Settings
            hidden = settings.Hidden
        except:
            hidden = '<unknown>'

        print('%s.' % n)
        print('Name          : %s' % task.Name)
        print('Path          : %s' % task.Path)
        print('Hidden        : %s' % hidden)
        print('State         : %s' % TASK_STATE[task.State])
        print('Enabled       : %s' % task.Enabled)
        print('Last Run      : %s' % task.LastRunTime)
        print('Last Result   : %s' % task.LastTaskResult)
        print('Next Run Time : %s' % task.NextRunTime)
        print('Number Of Missed Runs : %s' % task.NumberOfMissedRuns)

        actions = []
        try:
            for action in task.Definition.Actions:
                # TODO: Использовать типы на питоне
                actions.append(action)
                if action.Type == TASK_ACTION_EXEC:
                    print('TASK_ACTION_EXEC', action.Path, action.WorkingDirectory, action.Arguments, sep=' | ')
                elif action.Type == TASK_ACTION_COM_HANDLER:
                    print('TASK_ACTION_COM_HANDLER', action.ClassId, action.Data)
                elif action.Type == TASK_ACTION_SEND_EMAIL:
                    print('TASK_ACTION_SEND_EMAIL', action.To, action.Subject, action.Body)
                elif action.Type == TASK_ACTION_SHOW_MESSAGE:
                    print('TASK_ACTION_SHOW_MESSAGE', action.Title, action.MessageBody)
                else:
                    raise Exception(f'Unknown type: {action.Type}')
        except pywintypes.com_error:
            pass

        print('Actions : %s' % actions)
        print()

print('Listed %d tasks.' % n)
