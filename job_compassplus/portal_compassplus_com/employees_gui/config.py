#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


URL = "https://portal.compassplus.com/Employees/Pages/OfficeReferenceBook.aspx"
URL_GET_EMPLOYEES_LIST = (
    "https://portal.compassplus.com/_layouts/15/tbi/employees.ashx?"
    "p=50&c=1&s={}&fl=MPhotoUrl;NameLink;JobTitle;Department;WorkPhone"
)

URL_GET_EMPLOYEE_INFO = (
    "https://portal.compassplus.com/_layouts/15/tbi/ui.ashx?u={}"
    "&ctrl=TBI.SharePoint.Employees.WebParts/EmployeeFlyout"
)

SETTINGS_FILE_NAME = "settings"

PERSON_PLACEHOLDER_PHOTO = "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"
