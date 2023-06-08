#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""Скрипт добавляет метку 'исключения' для указанных вопросов."""


import json
import sys

from PySide.QtGui import QApplication

from web_tag_editor import WebTagEditor, get_logger


config = json.load(open("config", encoding="utf8"))
LOGIN = config["login"]
PASSWORD = config["password"]


logger = get_logger("so_questions")

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # TODO: удалять из базы измененный вопрос

    tag_editor = WebTagEditor(
        LOGIN, PASSWORD, "https://ru.stackoverflow.com/questions/504080"
    )
    tag_editor.show()
    tag_editor.go()

    sys.exit(app.exec_())
