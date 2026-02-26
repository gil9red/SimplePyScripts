#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from PyQt5.QtWidgets import *


class Widget(QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("Stack and Queue")

        self.list_widget_stack = QListWidget()
        self.list_widget_queue = QListWidget()

        self.spinbox_number = QSpinBox()

        self.push_button_push = QPushButton("Push")
        self.push_button_push.clicked.connect(self._on_push)

        self.push_button_pop = QPushButton("Pop")
        self.push_button_pop.clicked.connect(self._on_pop)

        self.radio_button_stack = QRadioButton("Stack")
        self.radio_button_stack.setChecked(True)

        self.radio_button_queue = QRadioButton("Queue")

        layout_list_widget_stack = QVBoxLayout()
        layout_list_widget_stack.addWidget(QLabel("Stack:"))
        layout_list_widget_stack.addWidget(self.list_widget_stack)

        layout_list_widget_queue = QVBoxLayout()
        layout_list_widget_queue.addWidget(QLabel("Queue:"))
        layout_list_widget_queue.addWidget(self.list_widget_queue)

        left_layout = QHBoxLayout()
        left_layout.addLayout(layout_list_widget_stack)
        left_layout.addLayout(layout_list_widget_queue)

        layout_group_box = QHBoxLayout()
        layout_group_box.addWidget(self.radio_button_stack)
        layout_group_box.addWidget(self.radio_button_queue)

        layout_buttons = QHBoxLayout()
        layout_buttons.addWidget(self.push_button_push)
        layout_buttons.addWidget(self.push_button_pop)

        group_box_select = QGroupBox("Select")
        group_box_select.setLayout(layout_group_box)

        right_layout = QVBoxLayout()
        right_layout.addWidget(group_box_select)
        right_layout.addWidget(self.spinbox_number)
        right_layout.addLayout(layout_buttons)
        right_layout.addStretch()

        main_layout = QHBoxLayout()
        main_layout.addLayout(left_layout)
        main_layout.addLayout(right_layout)

        self.setLayout(main_layout)

    def _on_push(self) -> None:
        number = str(self.spinbox_number.value())

        if self.radio_button_stack.isChecked():
            self.list_widget_stack.addItem(number)
        else:
            self.list_widget_queue.addItem(number)

        self.spinbox_number.setValue(self.spinbox_number.value() + 1)

    def _on_pop(self) -> None:
        if self.radio_button_stack.isChecked():
            self.list_widget_stack.takeItem(0)
        else:
            last_index = self.list_widget_queue.count() - 1
            self.list_widget_queue.takeItem(last_index)


if __name__ == "__main__":
    app = QApplication([])

    w = Widget()
    w.show()
    w.resize(600, 400)

    app.exec()
