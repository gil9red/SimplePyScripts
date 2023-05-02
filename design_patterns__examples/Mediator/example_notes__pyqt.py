#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: Design Patterns: Mediator — Посредник
# SOURCE: https://ru.wikipedia.org/wiki/Посредник_(шаблон_проектирования)
# SOURCE: https://refactoring.guru/ru/design-patterns/mediator/java/example


import traceback
import sys

from abc import abstractmethod
from typing import Any


try:
    from PyQt5.QtWidgets import *
    from PyQt5.QtCore import *

except:
    try:
        from PyQt4.QtGui import *
        from PyQt4.QtCore import *

    except:
        from PySide.QtGui import *
        from PySide.QtCore import *


def log_uncaught_exceptions(ex_cls, ex, tb):
    text = f"{ex_cls.__name__}: {ex}:\n"
    text += "".join(traceback.format_tb(tb))

    print(text)
    QMessageBox.critical(None, "Error", text)
    sys.exit(1)


sys.excepthook = log_uncaught_exceptions


# Класс заметок
class Note:
    def __init__(self):
        self._name = "note"
        self._text = ""

    def setName(self, name: str):
        self._name = name

    def setText(self, text: str):
        self._text = text

    def getName(self) -> str:
        return self._name

    def getText(self) -> str:
        return self._text


class DefaultListModel(QAbstractListModel):
    def __init__(self):
        super().__init__()

        self.items: list[Note] = []

    def rowCount(self, parent: QModelIndex = None):
        return len(self.items)

    def data(self, index: QModelIndex, role: int = Qt.DisplayRole) -> Any:
        if not index.isValid() or index.row() < 0 or index.row() >= self.rowCount():
            return QVariant()

        element = self.items[index.row()]

        if role == Qt.DisplayRole:
            return element.getName()

        return QVariant()

    def get_element(self, index: int) -> Note:
        return self.items[index]

    def addElement(self, element: Note):
        length = self.rowCount()

        self.beginInsertRows(QModelIndex(), length, length)
        self.items.append(element)
        self.endInsertRows()

        # Говорим view, что данные изменились
        self.dataChanged.emit(self.createIndex(length, 0), self.createIndex(length, 0))

    def removeElement(self, index: int):
        self.beginRemoveRows(QModelIndex(), index, index)
        self.items.pop(index)
        self.endRemoveRows()

        # Говорим view, что данные изменились
        self.dataChanged.emit(self.createIndex(index, 0), self.createIndex(index, 0))

    def get_items(self) -> list[Note]:
        return self.items


# Общий интерфейс посредников.
class Mediator:
    @abstractmethod
    def addNewNote(self, note: Note):
        pass

    @abstractmethod
    def deleteNote(self):
        pass

    @abstractmethod
    def getInfoFromList(self, note: Note):
        pass

    @abstractmethod
    def saveChanges(self):
        pass

    @abstractmethod
    def markNote(self):
        pass

    @abstractmethod
    def clear(self):
        pass

    @abstractmethod
    def sendToFilter(self, listModel: DefaultListModel):
        pass

    @abstractmethod
    def setElementsList(self, listModel: DefaultListModel):
        pass

    @abstractmethod
    def registerComponent(self, component: "Component"):
        pass

    @abstractmethod
    def hideElements(self, flag: bool):
        pass

    @abstractmethod
    def createGUI(self):
        pass


class Component:
    """Общий класс компонентов."""

    def __init__(self):
        self._mediator: Mediator = None

    def setMediator(self, mediator: Mediator):
        self._mediator = mediator

    @abstractmethod
    def getName(self) -> str:
        pass


# Конкретные компоненты никак не связаны между собой.  У них есть только один
# канал общения – через отправку уведомлений посреднику.
class AddButton(QPushButton, Component):
    def __init__(self):
        super().__init__("Add")

        # При клике на кнопку вызываем метод посредника
        self.clicked.connect(lambda: self._mediator.addNewNote(Note()))

    def getName(self) -> str:
        return "AddButton"


# Конкретные компоненты никак не связаны между собой.  У них есть только один
# канал общения – через отправку уведомлений посреднику.
class DeleteButton(QPushButton, Component):
    def __init__(self):
        super().__init__("Del")

        # При клике на кнопку вызываем метод посредника
        self.clicked.connect(lambda: self._mediator.deleteNote())

    def getName(self) -> str:
        return "DelButton"


# Конкретные компоненты никак не связаны между собой. У них есть только один
# канал общения – через отправку уведомлений посреднику.
class Filter(QLineEdit, Component):
    def __init__(self):
        super().__init__()

        self._listModel: DefaultListModel = None

    def setList(self, listModel: DefaultListModel):
        self._listModel = listModel

    def keyPressEvent(self, event: "QKeyEvent"):
        super().keyPressEvent(event)

        start = self.text()
        self._searchElements(start)

    def _searchElements(self, text: str):
        if self._listModel is None:
            return

        if text == "":
            self._mediator.setElementsList(self._listModel)
            return

        text = text.lower()
        notes = self._listModel.get_items()

        listModel = DefaultListModel()
        for note in notes:
            if text in note.getName().lower():
                listModel.addElement(note)

        self._mediator.setElementsList(listModel)

    def getName(self) -> str:
        return "Filter"


# Конкретные компоненты никак не связаны между собой. У них есть только один
# канал общения – через отправку уведомлений посреднику.
class ListNote(QListView, Component):
    def __init__(self, listModel: DefaultListModel):
        super().__init__()

        self._listModel = listModel
        self.setModel(self._listModel)

    def addElement(self, note: Note):
        self._listModel.addElement(note)
        index = self._listModel.rowCount() - 1
        index = self._listModel.index(index, 0)

        self.setCurrentIndex(index)

        self._mediator.sendToFilter(self._listModel)

    def deleteElement(self):
        if not self.currentIndex().isValid():
            return

        row = self.currentIndex().row()
        try:
            self._listModel.removeElement(row)
            self._mediator.sendToFilter(self._listModel)

        except IndexError:
            pass

    def getCurrentElement(self) -> Note:
        row = self.currentIndex().row()
        return self._listModel.get_element(row)

    def getName(self) -> str:
        return "List"


# Конкретные компоненты никак не связаны между собой. У них есть только один
# канал общения – через отправку уведомлений посреднику.
class SaveButton(QPushButton, Component):
    def __init__(self):
        super().__init__("Save")

        # При клике на кнопку вызываем метод посредника
        self.clicked.connect(lambda: self._mediator.saveChanges())

    def getName(self) -> str:
        return "SaveButton"


# Конкретные компоненты никак не связаны между собой. У них есть только один
# канал общения – через отправку уведомлений посреднику.
class TextBox(QTextEdit, Component):
    def keyPressEvent(self, event: "QKeyEvent"):
        super().keyPressEvent(event)

        self._mediator.markNote()

    def getName(self) -> str:
        return "TextBox"


# Конкретные компоненты никак не связаны между собой. У них есть только один
# канал общения – через отправку уведомлений посреднику.
class Title(QLineEdit, Component):
    def keyPressEvent(self, event: "QKeyEvent"):
        super().keyPressEvent(event)

        self._mediator.markNote()

    def getName(self) -> str:
        return "Title"


# Конкретный посредник. Все связи между конкретными компонентами переехали в
# код посредника. Он получает извещения от своих компонентов и знает как на них
# реагировать.
class Editor(Mediator):
    def __init__(self):
        self._title: Title      = None
        self._textBox: TextBox  = None
        self._add: AddButton    = None
        self._del: DeleteButton = None
        self._save: SaveButton  = None
        self._list: ListNote    = None
        self._filter: Filter    = None

        self._titleLabel = QLabel("Title:")
        self._textLabel = QLabel("Text:")
        self._label = QLabel("Add or select existing note to proceed...")

        self._mainWindow = None

    # Здесь происходит регистрация компонентов посредником.
    def registerComponent(self, component: Component):
        component.setMediator(self)

        if component.getName() == "AddButton":
            self._add = component

        elif component.getName() == "DelButton":
            self._del = component

        elif component.getName() == "Filter":
            self._filter = component

        elif component.getName() == "List":
            self._list: ListNote = component

            def foo(*args):
                empty = len(self._list.selectedIndexes()) == 0
                self.hideElements(empty)

                note = self._list.getCurrentElement()
                if note:
                    self.getInfoFromList(note)

            # Вызываем нашу функцию при изменении выделения элементов в списке
            self._list.clicked.connect(foo)

        elif component.getName() == "SaveButton":
            self._save = component

        elif component.getName() == "TextBox":
            self._textBox = component

        elif component.getName() == "Title":
            self._title = component

    #
    # Разнообразные методы общения с компонентами.
    #

    def addNewNote(self, note: Note):
        # Инкрементальные названия
        text = note.getName() + str(self._list.model().rowCount() + 1)
        note.setName(text)

        self._title.setText("")
        self._textBox.setText("")
        self._list.addElement(note)

    def deleteNote(self):
        self._list.deleteElement()

    def getInfoFromList(self, note: Note):
        self._title.setText(note.getName().replace("*", " "))
        self._textBox.setText(note.getText())

    def saveChanges(self):
        try:
            note = self._list.getCurrentElement()
            note.setName(self._title.text())
            note.setText(self._textBox.toPlainText())

            self._list.update()

        except Exception:
            traceback.print_exc()

    def markNote(self):
        try:
            note = self._list.getCurrentElement()
            name = note.getName()
            if not name.endswith("*"):
                note.setName(note.getName() + "*")

            self._list.update()
            # NOTE: Правильно сделать через сигнал модели для view. К тому же, это намного быстрее работает чем
            #       update()
            # self._list.model().dataChanged.emit(self._list.model().index(0, 0), self._list.model().index(0, 0))

        except Exception:
            traceback.print_exc()

    def clear(self):
        self._title.setText("")
        self._textBox.setText("")

    def sendToFilter(self, listModel: DefaultListModel):
        self._filter.setList(listModel)

    def setElementsList(self, listModel: DefaultListModel):
        self._list.setModel(listModel)
        self._list.update()

    def hideElements(self, flag: bool):
        self._titleLabel.setVisible(not flag)
        self._textLabel.setVisible(not flag)
        self._title.setVisible(not flag)
        self._textBox.setVisible(not flag)
        self._save.setVisible(not flag)
        self._label.setVisible(flag)

    def createGUI(self):
        # notes_side
        notes_side_filter_layout = QHBoxLayout()
        notes_side_filter_layout.addWidget(QLabel("Filter:"))
        notes_side_filter_layout.addWidget(self._filter)

        notes_side_buttons_layout = QHBoxLayout()
        notes_side_buttons_layout.addWidget(self._add)
        notes_side_buttons_layout.addWidget(self._del)

        notes_side_main_layout = QVBoxLayout()
        notes_side_main_layout.addLayout(notes_side_filter_layout)
        notes_side_main_layout.addWidget(self._list)
        notes_side_main_layout.addLayout(notes_side_buttons_layout)

        notes_side = QWidget()
        notes_side.setLayout(notes_side_main_layout)
        # notes_side

        # notes_editor
        notes_editor_header_layout = QHBoxLayout()
        notes_editor_header_layout.addWidget(self._titleLabel)
        notes_editor_header_layout.addWidget(self._title)

        notes_editor_main_layout = QVBoxLayout()
        notes_editor_main_layout.addWidget(self._label)
        notes_editor_main_layout.addLayout(notes_editor_header_layout)
        notes_editor_main_layout.addWidget(self._textLabel)
        notes_editor_main_layout.addWidget(self._textBox)
        notes_editor_main_layout.addWidget(self._save)

        notes_editor = QWidget()
        notes_editor.setLayout(notes_editor_main_layout)
        # notes_editor

        splitter = QSplitter()
        splitter.addWidget(notes_side)
        splitter.addWidget(notes_editor)

        self._mainWindow = QMainWindow()
        self._mainWindow.setWindowTitle("Notes")
        self._mainWindow.setCentralWidget(splitter)

        # По умолчанию прячем элементы в редакторе заметки
        self.hideElements(flag=True)

        self._mainWindow.show()


if __name__ == "__main__":
    app = QApplication([])

    mediator = Editor()

    mediator.registerComponent(Title())
    mediator.registerComponent(TextBox())
    mediator.registerComponent(AddButton())
    mediator.registerComponent(DeleteButton())
    mediator.registerComponent(SaveButton())
    mediator.registerComponent(ListNote(DefaultListModel()))
    mediator.registerComponent(Filter())

    mediator.createGUI()

    app.exec()
