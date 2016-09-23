#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import config


def get_url(page):
    return config.URL_GET_EMPLOYEES_LIST.format((page - 1) * 50)


from db import *

import requests
from requests_ntlm import HttpNtlmAuth


session = requests.Session()
session.auth = HttpNtlmAuth(config.LOGIN, config.PASSWORD, session)


def fill_db():
    # Авторизация
    rs = session.get(config.URL)
    if not rs.ok:
        print('Не удалось авторизоваться')
        print('rs.status_code = {}'.format(rs.status_code))
        print('rs.headers = {}'.format(rs.headers))
        return

    page = 1

    rs = session.get(get_url(page))
    data = rs.json()

    max_page = data['Pages']

    employee_list = list()
    employee_list += data['Properties']

    while page < max_page:
        page += 1

        rs = session.get(get_url(page))
        data = rs.json()

        employee_list += data['Properties']

    for i, row in enumerate(employee_list, 1):
        employee_id = row['Id']

        if exists(employee_id):
            print('Employee with id = {} already exist.'.format(employee_id))
            continue

        rs = session.get(config.URL_GET_EMPLOYEE_INFO.format(employee_id))
        if not rs.ok:
            print("Request getting employee info (id={}) not ok.".format(employee_id))
            print("rs.status_code = {}".format(rs.status_code))
            print("rs.headers = {}".format(rs.headers))
            continue

        employee = Employee.parse(rs.text, session)
        print(i, employee)

        db_session.add(employee)

    db_session.commit()


# # TODO: показывать короткое имя пользователя: ipetrash, ypaliy и т.п.
#
# if __name__ == '__main__':
#     fill_db()


from qtpy.QtGui import *
from qtpy.QtWidgets import *
from qtpy.QtCore import *

import base64


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
            # TODO: нужно показывать какое-то изображение по умолчанию, например, то которое самой системой
            # используется, т.к. есть те, у кого фотки нет
            self.photo.clear()
            self.photo.setText("None")

            self.name.setText("None")
            self.short_name.setText("None")
            self.job.setText("None")
            self.department.setText("None")
            self.birthday.setText("None")
            self.url.setText("None")
            self.work_phone.setText("None")
            self.mobile_phone.setText("None")
            self.email.setText("None")
            return

        pixmap = QPixmap()
        pixmap.loadFromData(base64.b64decode(employee.photo.encode()))
        pixmap = pixmap.scaledToWidth(192, Qt.SmoothTransformation)
        self.photo.setPixmap(pixmap)

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


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Compass Plus Employees')
        self.setContextMenuPolicy(Qt.NoContextMenu)

        # TODO: добавить кнопку очистки редактора
        # TODO: добавить кнопку перечитывания всей таблицы
        # TODO: окно с информацией о выделенном сотруднике умеет показывать его переработку/недоработку и прочее
        self.filter_line_edit = QLineEdit()
        self.filter_line_edit.textEdited.connect(self.run_filter)

        self.employees_table = QTableWidget()
        self.employees_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.employees_table.setSelectionMode(QTableWidget.SingleSelection)
        self.employees_table.currentItemChanged.connect(lambda item, _: self._item_click(item))

        layout_filter = QHBoxLayout()
        layout_filter.addWidget(QLabel('Filter:'))
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

        # tool_bar = self.addToolBar('Основное')
        # action_reload = tool_bar.addAction("Перечитать все гисты пользователя")
        # action_reload.setToolTip('Удаление текущих гистов и подгрузка новых')
        # action_reload.setStatusTip(action_reload.toolTip())
        # action_reload.triggered.connect(self.reload)
        #
        # action_sync = tool_bar.addAction("Синхронизация")
        # action_sync.setToolTip('Удаление уже несуществующих гистов и добавление новых')
        # action_sync.setStatusTip(action_reload.toolTip())
        # action_sync.triggered.connect(self.sync)
        #
        # self.setStatusBar(QStatusBar())

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
        from sqlalchemy import or_
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
            "Name", "Short Name", "Job", "Department",
            "Birthday", "Url", "Work Phone", "Mobile Phone", "Id", "Email", "Photo"
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
            self.employees_table.setItem(row, 7, QTableWidgetItem(employee.mobile_phone))
            self.employees_table.setItem(row, 8, QTableWidgetItem(employee.id))
            self.employees_table.setItem(row, 9, QTableWidgetItem(employee.email))
            self.employees_table.setItem(row, 10, QTableWidgetItem(employee.photo))

            self.employees_table.item(row, 0).setData(Qt.UserRole, employee)

            row += 1

        # Показываем информацию о первом сотруднике
        if self.employees_table.rowCount() > 0:
            item = self.employees_table.item(0, 0)
            self.employees_table.setCurrentItem(item)

    def read_settings(self):
        # TODO: при сложных настройках, лучше перейти на json или yaml
        ini = QSettings(config.SETTINGS_FILE_NAME, QSettings.IniFormat)

        state = ini.value('MainWindow_State')
        if state:
            self.restoreState(state)

        geometry = ini.value('MainWindow_Geometry')
        if geometry:
            self.restoreGeometry(geometry)

    def write_settings(self):
        ini = QSettings(config.SETTINGS_FILE_NAME, QSettings.IniFormat)
        ini.setValue('MainWindow_State', self.saveState())
        ini.setValue('MainWindow_Geometry', self.saveGeometry())

    def closeEvent(self, _):
        self.write_settings()

        QApplication.instance().quit()


if __name__ == '__main__':
    app = QApplication([])

    mw = MainWindow()
    mw.resize(1000, 750)
    mw.read_settings()
    mw.show()
    mw.run_filter()
    # TODO:
    mw.employees_table.setFocus()

    app.exec_()
