#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import base64
import sys
import traceback

import requests

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from requests_ntlm2 import HttpNtlmAuth

from sqlalchemy import or_

import config
from db import *


# Для отлова всех исключений, которые в слотах Qt могут "затеряться" и привести к тихому падению
def log_uncaught_exceptions(ex_cls, ex, tb):
    text = f"{ex_cls.__name__}: {ex}:\n"
    text += "".join(traceback.format_tb(tb))

    print("Error: ", text)
    QMessageBox.critical(None, "Error", text)
    sys.exit(1)


sys.excepthook = log_uncaught_exceptions


def get_url(page):
    return config.URL_GET_EMPLOYEES_LIST.format((page - 1) * 50)


# # TODO: показывать короткое имя пользователя: ipetrash, ypaliy и т.п.
#
# if __name__ == '__main__':
#     fill_db()


def pixmap_from_base64(base64_text):
    pixmap = QPixmap()
    pixmap.loadFromData(base64.b64decode(base64_text))
    pixmap = pixmap.scaledToWidth(192, Qt.SmoothTransformation)

    return pixmap


class EmployeeInfo(QWidget):
    def __init__(self):
        super().__init__()

        self.photo = QLabel()
        self.name = QLabel()
        self.short_name = QLabel()
        self.job = QLabel()
        self.department = QLabel()
        # TODO: показывать также сколько осталось до др
        self.birthday = QLabel()

        self.url = QLabel()
        self.url.setOpenExternalLinks(True)

        self.work_phone = QLabel()
        self.mobile_phone = QLabel()
        self.id = QLabel()

        self.email = QLabel()
        self.email.setOpenExternalLinks(True)

        form_layout = QFormLayout()
        form_layout.addRow("Name:", self.name)
        form_layout.addRow("Short Name:", self.short_name)
        form_layout.addRow("Job:", self.job)
        form_layout.addRow("Department:", self.department)
        form_layout.addRow("Birthday:", self.birthday)
        form_layout.addRow("Url:", self.url)
        form_layout.addRow("Work Phone:", self.work_phone)
        form_layout.addRow("Mobile Phone:", self.mobile_phone)
        form_layout.addRow("Id:", self.id)
        form_layout.addRow("Email:", self.email)

        layout = QVBoxLayout()
        layout.addWidget(self.photo)
        layout.addLayout(form_layout)
        layout.addStretch()

        scroll_area_widget = QWidget()
        scroll_area_widget.setLayout(layout)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(scroll_area_widget)

        layout = QVBoxLayout()
        layout.addWidget(scroll_area)
        self.setLayout(layout)

        # Все QLabel на форме умеет поддержку выделения и при наличии ссылок на них можно кликать
        for label in self.findChildren(QLabel):
            label.setTextInteractionFlags(Qt.TextBrowserInteraction)

    def set_employee(self, employee):
        if not employee:
            self.photo.setPixmap(pixmap_from_base64(config.PERSON_PLACEHOLDER_PHOTO))

            self.name.setText("None")
            self.short_name.setText("None")
            self.job.setText("None")
            self.department.setText("None")
            self.birthday.setText("None")
            self.url.setText("None")
            self.work_phone.setText("None")
            self.mobile_phone.setText("None")
            self.id.setText("None")
            self.email.setText("None")
            return

        self.photo.setPixmap(pixmap_from_base64(employee.photo))

        self.name.setText(employee.name)
        self.short_name.setText(employee.short_name)
        self.job.setText(employee.job)
        self.department.setText(employee.department)
        self.birthday.setText(employee.birthday)
        self.url.setText('<a href="{0}">{0}</a>'.format(employee.url))
        self.work_phone.setText(employee.work_phone)
        self.mobile_phone.setText(employee.mobile_phone)
        self.id.setText(employee.id)
        self.email.setText('<a href="mailto:{0}">{0}</a>'.format(employee.email))


# TODO: ввод с клавы при фокусе на таблицу меняет редактор фильтра
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Compass Plus Employees")
        self.setContextMenuPolicy(Qt.NoContextMenu)

        # TODO: окно с информацией о выделенном сотруднике умеет показывать его переработку/недоработку и прочее
        self.filter_line_edit = QLineEdit()
        # При изменении окна происходит вызов run_filter и отображение/скрытие кнопки очистки текста
        self.filter_line_edit.textChanged.connect(self.run_filter)
        self.filter_line_edit.installEventFilter(self)

        try:
            # Добавление в редактор фильтра кнопки очищения содержимого
            clear_icon = self.style().standardIcon(QStyle.SP_LineEditClearButton)

            clear_action = self.filter_line_edit.addAction(
                clear_icon, QLineEdit.TrailingPosition
            )
            clear_action.setVisible(len(self.filter_line_edit.text()) > 0)
            clear_action.triggered.connect(self.filter_line_edit.clear)

            self.filter_line_edit.textChanged.connect(
                lambda text: clear_action.setVisible(len(text) > 0)
            )

        # Если SP_LineEditClearButton не найден
        except AttributeError:
            # TODO: сделать реализацию для Qt4
            # clear_icon = pixmap_from_base64(config.LINE_EDIT_CLEAR_BUTTON_32x32)
            pass

        self.employees_table = QTableWidget()
        self.employees_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.employees_table.setSelectionMode(QTableWidget.SingleSelection)
        self.employees_table.currentItemChanged.connect(
            lambda item, _: self._item_click(item)
        )

        layout_filter = QHBoxLayout()
        layout_filter.addWidget(QLabel("Filter:"))
        layout_filter.addWidget(self.filter_line_edit)

        layout = QVBoxLayout()
        layout.addLayout(layout_filter)
        layout.addWidget(self.employees_table)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        employee_info_dock_widget = QDockWidget("Employee Info")
        employee_info_dock_widget.setObjectName("employee_info_dock_widget")
        employee_info_dock_widget.setFeatures(QDockWidget.NoDockWidgetFeatures)

        self.employee_info = EmployeeInfo()
        employee_info_dock_widget.setWidget(self.employee_info)
        self.addDockWidget(Qt.RightDockWidgetArea, employee_info_dock_widget)

        tool_bar = self.addToolBar("General")
        tool_bar.setObjectName("General")
        action_refill = tool_bar.addAction("Parse and refill")
        action_refill.setToolTip(
            "Clear database, parse site with employees, and fill database"
        )
        action_refill.setStatusTip(action_refill.toolTip())
        action_refill.triggered.connect(self.refill)

        self.setStatusBar(QStatusBar())

    def refill(self):
        # TODO: можно в отдельный класс вынести
        dialog = QDialog()
        dialog.setWindowTitle("Auth and refill database")

        info = QLabel()
        info.setText(
            """When you click on OK, you will be cleansing a database of employees,
start parsing for the collection of employees and populate the database."""
        )

        login = QLineEdit("CP\\")
        password = QLineEdit()
        password.setEchoMode(QLineEdit.Password)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)

        form_layout = QFormLayout()
        form_layout.addRow("Login:", login)
        form_layout.addRow("Password:", password)

        layout = QVBoxLayout()
        layout.addWidget(info)
        layout.addLayout(form_layout)
        layout.addStretch()
        layout.addWidget(button_box)

        dialog.setLayout(layout)
        if not dialog.exec():
            return

        login, password = login.text(), password.text()

        # Сначала пытаемся авторизоваться
        session = requests.Session()
        session.auth = HttpNtlmAuth(login, password, session)

        # Авторизация
        rs = session.get(config.URL)
        if not rs.ok:
            QMessageBox.information(self, "Info", "Failed to login")
            print("Не удалось авторизоваться")
            print("rs.status_code = {}".format(rs.status_code))
            print("rs.headers = {}".format(rs.headers))
            return

        # TODO: move to db.py
        # Очищение базы данных
        for i in db_session.query(Employee):
            db_session.delete(i)
        db_session.commit()

        self.run_filter()
        self.fill_db(session)
        self.run_filter()

    def fill_db(self, session):
        page = 1

        rs = session.get(get_url(page))
        data = rs.json()

        max_page = data["Pages"]

        # TODO: наверное тоже нужно в QProgressDialog обернуть, хоть сбор и быстрый
        employee_list = list()
        employee_list += data["Properties"]

        while page < max_page:
            page += 1

            rs = session.get(get_url(page))
            data = rs.json()

            employee_list += data["Properties"]

        # Для отображения диалога парсинга и заполнения базы
        progress = QProgressDialog(
            "Operation in progress...", "Cancel", 0, len(employee_list), self
        )
        progress.setWindowTitle("Parsing")
        progress.setWindowModality(Qt.WindowModal)

        for i, row in enumerate(employee_list, 1):
            progress.setValue(i)

            if progress.wasCanceled():
                break

            employee_id = row["Id"]

            if exists(employee_id):
                print("Employee with id = {} already exist.".format(employee_id))
                continue

            rs = session.get(config.URL_GET_EMPLOYEE_INFO.format(employee_id))
            if not rs.ok:
                print(
                    "Request getting employee info (id={}) not ok.".format(employee_id)
                )
                print("rs.status_code = {}".format(rs.status_code))
                print("rs.headers = {}".format(rs.headers))
                continue

            employee = Employee.parse(rs.text, session)
            print(i, employee)

            db_session.add(employee)

        db_session.commit()

        progress.setValue(len(employee_list))

    def _item_click(self, item):
        employee = None

        if item and self.employees_table.rowCount() > 0:
            item = self.employees_table.item(item.row(), 0)
            employee = item.data(Qt.UserRole)

        self.employee_info.set_employee(employee)

    def run_filter(self):
        # TODO: лучше использовать модель
        # TODO: лучше использовать стандартный фильтр qt
        # TODO: поиграться с делегатами для красивого отображения описания + ссылки на гист

        self.employees_table.clear()
        self._item_click(None)

        # TODO: db.py
        filter_text = self.filter_line_edit.text()
        filter_text = "%{}%".format(filter_text)
        sql_filter = or_(
            Employee.name.like(filter_text),
            Employee.short_name.like(filter_text),
            Employee.job.like(filter_text),
            Employee.department.like(filter_text),
            Employee.birthday.like(filter_text),
            Employee.work_phone.like(filter_text),
            Employee.mobile_phone.like(filter_text),
            Employee.id.like(filter_text),
            Employee.email.like(filter_text),
        )

        query = db_session.query(Employee).filter(sql_filter)
        rows = query.count()

        self.employees_table.setRowCount(rows)

        headers = [
            "Name",
            "Short Name",
            "Job",
            "Department",
            "Birthday",
            "Url",
            "Work Phone",
            "Mobile Phone",
            "Id",
            "Email",
            "Photo",
        ]
        self.employees_table.setColumnCount(len(headers))
        self.employees_table.setHorizontalHeaderLabels(headers)

        row = 0
        for employee in query:
            self.employees_table.setItem(row, 0, QTableWidgetItem(employee.name))
            self.employees_table.setItem(row, 1, QTableWidgetItem(employee.short_name))
            self.employees_table.setItem(row, 2, QTableWidgetItem(employee.job))
            self.employees_table.setItem(row, 3, QTableWidgetItem(employee.department))
            self.employees_table.setItem(row, 4, QTableWidgetItem(employee.birthday))
            self.employees_table.setItem(row, 5, QTableWidgetItem(employee.url))
            self.employees_table.setItem(row, 6, QTableWidgetItem(employee.work_phone))
            self.employees_table.setItem(
                row, 7, QTableWidgetItem(employee.mobile_phone)
            )
            self.employees_table.setItem(row, 8, QTableWidgetItem(employee.id))
            self.employees_table.setItem(row, 9, QTableWidgetItem(employee.email))
            self.employees_table.setItem(row, 10, QTableWidgetItem(employee.photo))

            self.employees_table.item(row, 0).setData(Qt.UserRole, employee)

            row += 1

        # Запрет редактирования ячеек таблицы
        for row in range(self.employees_table.rowCount()):
            for column in range(self.employees_table.columnCount()):
                self.employees_table.item(row, column).setFlags(
                    Qt.ItemIsSelectable | Qt.ItemIsEnabled
                )

        # Показываем информацию о первом сотруднике
        if self.employees_table.rowCount() > 0:
            item = self.employees_table.item(0, 0)
            self.employees_table.setCurrentItem(item)

    def read_settings(self):
        ini = QSettings(config.SETTINGS_FILE_NAME, QSettings.IniFormat)

        state = ini.value("MainWindow_State")
        if state:
            self.restoreState(state)

        geometry = ini.value("MainWindow_Geometry")
        if geometry:
            self.restoreGeometry(geometry)

    def write_settings(self):
        ini = QSettings(config.SETTINGS_FILE_NAME, QSettings.IniFormat)
        ini.setValue("MainWindow_State", self.saveState())
        ini.setValue("MainWindow_Geometry", self.saveGeometry())

    def eventFilter(self, object, event):
        # В окне вводе при клике на стрелку вниз фокус переходит в таблицу
        if object == self.filter_line_edit:
            if event.type() == QEvent.KeyRelease and event.key() == Qt.Key_Down:
                self.employees_table.setFocus()
                return False

        return super().eventFilter(object, event)

    def closeEvent(self, _):
        self.write_settings()

        QApplication.instance().quit()


if __name__ == "__main__":
    app = QApplication([])

    mw = MainWindow()
    mw.resize(1000, 750)
    mw.read_settings()
    mw.show()
    mw.run_filter()
    # TODO:
    mw.employees_table.setFocus()

    app.exec_()
