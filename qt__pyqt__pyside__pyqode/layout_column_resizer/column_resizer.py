#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://github.com/agateau/columnresizer


from dataclasses import dataclass

from PyQt5.QtCore import QEvent, QTimer, QSize, QRect, Qt, QObject, qCritical
from PyQt5.QtWidgets import (
    QFormLayout,
    QGridLayout,
    QWidget,
    QWidgetItem,
    QLayout,
    QLayoutItem,
)


class FormLayoutWidgetItem(QWidgetItem):
    def __init__(
        self,
        widget: QWidget,
        formLayout: QFormLayout,
        itemRole: QFormLayout.ItemRole,
    ) -> None:
        super().__init__(widget)

        self.m_width: int = -1
        self.m_formLayout: QFormLayout = formLayout
        self.m_itemRole: QFormLayout.ItemRole = itemRole

    def sizeHint(self) -> QSize:
        size: QSize = super().sizeHint()
        if self.m_width != -1:
            size.setWidth(self.m_width)

        return size

    def minimumSize(self) -> QSize:
        size: QSize = super().minimumSize()
        if self.m_width != -1:
            size.setWidth(self.m_width)

        return size

    def maximumSize(self) -> QSize:
        size: QSize = super().maximumSize()
        if self.m_width != -1:
            size.setWidth(self.m_width)

        return size

    def setWidth(self, width: int) -> None:
        if width != self.m_width:
            self.m_width = width
            self.invalidate()

    def setGeometry(self, _rect: QRect) -> None:
        rect: QRect = _rect
        width = self.widget().sizeHint().width()
        if (
            self.m_itemRole == QFormLayout.LabelRole
            and self.m_formLayout.labelAlignment() & Qt.AlignRight
        ):
            rect.setLeft(rect.right() - width)

        super().setGeometry(rect)

    def formLayout(self) -> QFormLayout:
        return self.m_formLayout


@dataclass
class GridColumnInfo:
    layout: QGridLayout
    column: int


class ColumnResizerPrivate:
    def __init__(self, q_ptr: "ColumnResizer") -> None:
        self.q: ColumnResizer = q_ptr

        self.m_widgets: list[QWidget] = []
        self.m_wrWidgetItemList: list[FormLayoutWidgetItem] = []
        self.m_gridColumnInfoList: list[GridColumnInfo] = []

        self.m_updateTimer: QTimer = QTimer(self.q)
        self.m_updateTimer.setSingleShot(True)
        self.m_updateTimer.setInterval(0)
        self.m_updateTimer.timeout.connect(self.q.updateWidth)

    def scheduleWidthUpdate(self) -> None:
        self.m_updateTimer.start()


class ColumnResizer(QObject):
    def __init__(self, parent: QObject) -> None:
        super().__init__(parent)

        self.d = ColumnResizerPrivate(self)

    def addWidget(self, widget: QWidget) -> None:
        self.d.m_widgets.append(widget)
        widget.installEventFilter(self)
        self.d.scheduleWidthUpdate()

    # NOTE: Here the logic is changed relative to the original
    def updateWidth(self) -> None:
        width: int = 0
        x: int = 0
        for widget in self.d.m_widgets:
            x = max(widget.pos().x(), x)
            width = max(widget.sizeHint().width(), width)

        width += x

        for item in self.d.m_wrWidgetItemList:
            item.setWidth(width - item.widget().pos().x())
            item.formLayout().update()

        for info in self.d.m_gridColumnInfoList:
            info.layout.setColumnMinimumWidth(info.column, width)

    def eventFilter(self, _: QObject, event: QEvent) -> bool:
        if event.type() == QEvent.Resize:
            self.d.scheduleWidthUpdate()

        return False

    def addWidgetsFromLayout(self, layout: QLayout, column: int) -> None:
        assert column >= 0

        if isinstance(layout, QGridLayout):
            self.addWidgetsFromGridLayout(layout, column)
        elif isinstance(layout, QFormLayout):
            if column > QFormLayout.ItemRole.SpanningRole:
                qCritical(
                    f"column should not be more than {QFormLayout.ItemRole.SpanningRole} for QFormLayout"
                )
                return

            role: QFormLayout.ItemRole = QFormLayout.ItemRole(column)
            self.addWidgetsFromFormLayout(layout, role)
        else:
            qCritical(f"Don't know how to handle layout {layout}")

    def addWidgetsFromGridLayout(self, layout: QGridLayout, column: int) -> None:
        for row in range(layout.rowCount()):
            item: QLayoutItem = layout.itemAtPosition(row, column)
            if not item:
                continue

            widget: QWidget = item.widget()
            if not widget:
                continue

            self.addWidget(widget)

        self.d.m_gridColumnInfoList.append(GridColumnInfo(layout, column))

    def addWidgetsFromFormLayout(self, layout: QFormLayout, role: QFormLayout.ItemRole) -> None:
        for row in range(layout.rowCount()):
            item: QLayoutItem = layout.itemAt(row, role)
            if not item:
                continue

            widget: QWidget = item.widget()
            if not widget:
                continue

            layout.removeItem(item)
            newItem: FormLayoutWidgetItem = FormLayoutWidgetItem(widget, layout, role)
            layout.setItem(row, role, newItem)
            self.addWidget(widget)
            self.d.m_wrWidgetItemList.append(newItem)
