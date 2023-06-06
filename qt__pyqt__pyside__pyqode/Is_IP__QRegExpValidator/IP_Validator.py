#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from PyQt5.QtGui import QRegularExpressionValidator
from PyQt5.QtCore import QRegularExpression

from is_ip import IP_REGEXP


def get_ip_validator() -> QRegularExpressionValidator:
    return QRegularExpressionValidator(QRegularExpression(IP_REGEXP))
