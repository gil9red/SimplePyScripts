#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import sys

from PySide.QtGui import *
from PySide.QtCore import *
from PySide.QtXml import *


TREE_CONFIG = "tree.xml"


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("tree_model")

        self.model = QStandardItemModel()
        self.model.setColumnCount(1)
        self.model.setHorizontalHeaderLabels(["Animals"])

        self.view = QTreeView()
        self.view.setModel(self.model)

        self.pb_add = QPushButton("Add")
        self.pb_add.clicked.connect(self.add)

        self.pb_add_child = QPushButton("Add Child")
        self.pb_add_child.clicked.connect(self.add_child)

        self.pb_remove = QPushButton("Remove")
        self.pb_remove.clicked.connect(self.remove)

        self.pb_save_tree = QPushButton("Save tree")
        self.pb_save_tree.clicked.connect(self.save_tree)

        self.pb_restore_tree = QPushButton("Restore tree")
        self.pb_restore_tree.clicked.connect(self.restore_tree)

        layout = QVBoxLayout()
        layout.addWidget(self.view)

        button_layout = QGridLayout()
        button_layout.addWidget(self.pb_add, 1, 0)
        button_layout.addWidget(self.pb_add_child, 1, 1)
        button_layout.addWidget(self.pb_remove, 1, 2)
        button_layout.addWidget(self.pb_save_tree, 2, 0)
        button_layout.addWidget(self.pb_restore_tree, 2, 1)

        layout.addLayout(button_layout)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        # Создаем заранее набор
        item = QStandardItem("animals")
        self.model.appendRow(item)

        item = QStandardItem("animals")
        self.model.appendRow(item)
        item.appendRow(QStandardItem("dog"))

        child = QStandardItem("cat")
        child.appendRow(QStandardItem("Barsik"))
        child.appendRow(QStandardItem("Sharik"))
        item.appendRow(child)

        item = QStandardItem("animals")
        self.model.appendRow(item)

        self.view.expandAll()

    def add(self) -> None:
        item = QStandardItem("animals")
        self.model.appendRow(item)

    def add_child(self) -> None:
        child = QStandardItem("dog")

        index = self.view.currentIndex()
        if index is not None and index.isValid():
            item = self.model.itemFromIndex(index)
            item.appendRow(child)

            self.view.setExpanded(item.index(), True)

    def remove(self) -> None:
        index = self.view.currentIndex()
        if index is not None and index.isValid():
            self.model.removeRow(index.row(), index.parent())

    def create_xml(self, root_item, root_xml, doc) -> None:
        # Перебор детей элемента
        for row in range(root_item.rowCount()):
            child = root_item.child(row)

            tag = doc.createElement("Animal")
            tag.setAttribute("name", child.text())
            root_xml.appendChild(tag)

            self.create_xml(child, tag, doc)

    def save_tree(self) -> None:
        # Рекурсивный перебор дерева
        root = self.model.invisibleRootItem()

        doc = QDomDocument()
        xml_root = doc.createElement("Animals")
        doc.appendChild(xml_root)

        self.create_xml(root, xml_root, doc)

        file = QFile(TREE_CONFIG)
        if file.open(QIODevice.WriteOnly):
            xml = doc.toString(4)
            print(xml)
            file.write(xml)

        file.close()

    def create_item_model(self, item_root, xml_root) -> None:
        children = xml_root.childNodes()
        for i in range(children.count()):
            xml_child = children.item(i)
            name = xml_child.toElement().attribute("name")

            item_child = QStandardItem(name)
            item_root.appendRow(item_child)

            if xml_child.hasChildNodes():
                self.create_item_model(item_child, xml_child)

    def restore_tree(self) -> None:
        self.model.clear()
        self.model.setHorizontalHeaderLabels(["Animals"])

        doc = QDomDocument()
        file = QFile(TREE_CONFIG)
        if not file.open(QIODevice.ReadOnly):
            file.close()
            return

        if not doc.setContent(file):
            file.close()

        file.close()

        print(doc.toString(4))

        root = doc.documentElement()
        self.create_item_model(self.model.invisibleRootItem(), root)

        self.view.expandAll()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    mw = MainWindow()
    mw.show()

    sys.exit(app.exec_())
