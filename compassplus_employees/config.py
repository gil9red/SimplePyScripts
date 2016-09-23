#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


LOGIN = '<LOGIN>'
PASSWORD = '<PASSWORD>'

URL = 'https://portal.compassplus.com/Employees/Pages/OfficeReferenceBook.aspx'
URL_GET_EMPLOYEES_LIST = 'https://portal.compassplus.com/_layouts/15/tbi/employees.ashx?' \
                         'p=50&c=1&s={}&fl=MPhotoUrl;NameLink;JobTitle;Department;WorkPhone'

URL_GET_EMPLOYEE_INFO = 'https://portal.compassplus.com/_layouts/15/tbi/ui.ashx?u={}' \
                        '&ctrl=TBI.SharePoint.Employees.WebParts/EmployeeFlyout'

SETTINGS_FILE_NAME = 'settings'
