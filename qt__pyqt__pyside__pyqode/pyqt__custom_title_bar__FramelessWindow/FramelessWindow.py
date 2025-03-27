#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created on 2018年4月30日
# author: Irony
# site: https://github.com/892768447
# email: 892768447@qq.com
# file: FramelessWindow
# description:
# __author__ = """By: Irony
# QQ: 892768447
# Email: 892768447@qq.com"""
# __copyright__ = "Copyright (c) 2018 Irony"
# __version__ = 1.0

# SOURCE: https://github.com/892768447/PyQt/blob/f6ff3ee8bf8e7e9dd8d3ba3d39cf5cefa3c91e7b/%E6%97%A0%E8%BE%B9%E6%A1%86%E8%87%AA%E5%AE%9A%E4%B9%89%E6%A0%87%E9%A2%98%E6%A0%8F%E7%AA%97%E5%8F%A3/FramelessWindow.py

# Modified on 2025-03-32
# author: ipetrash
__author__ = "Irony, ipetrash"
__version__ = "1.1"
__copyright__ = "Copyright (c) 2018 Irony\nCopyright (c) 2025 ipetrash"


from enum import Enum, auto

from PyQt5.QtCore import Qt, pyqtSignal, QPoint, QEvent, QObject
from PyQt5.QtGui import (
    QEnterEvent,
    QPainter,
    QColor,
    QPen,
    QIcon,
    QFontMetrics,
    QMouseEvent,
    QPaintEvent,
)
from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QAbstractButton,
    QLabel,
    QToolButton,
    QStyle,
)


# SOURCE: https://github.com/gil9red/SimplePyScripts/blob/29b1f87e4381c398d906261b98c2ecf8c9933646/qt__pyqt__pyside__pyqode/ElidedLabel.py
class ElidedLabel(QLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setMinimumWidth(50)

    def paintEvent(self, event):
        painter = QPainter(self)

        metrics = QFontMetrics(self.font())
        elided_text = metrics.elidedText(self.text(), Qt.ElideRight, self.width())

        painter.drawText(self.rect(), self.alignment(), elided_text)


# Стиль
STYLE_SHEET = """
TitleBar {
    background-color: rgb(54, 157, 180);
}

TitleBar #buttonMinimum,
TitleBar #buttonMaximum,
TitleBar #buttonClose,
TitleBar #buttonPin
{
    color: black;
    border: none;
    background-color: rgb(54, 157, 180);
}
TitleBar #buttonPin:checked {
    /* TODO: жирным и рамку добавить */ 
    background-color: rgb(48, 141, 162);
}

TitleBar #buttonMinimum:hover,
TitleBar #buttonMaximum:hover,
TitleBar #buttonPin:hover
{
    background-color: rgb(48, 141, 162);
}
TitleBar #buttonClose:hover {
    color: white;
    background-color: red;
}

TitleBar #buttonMinimum:pressed,
TitleBar #buttonMaximum:pressed,
TitleBar #buttonPin:pressed
{
    background-color: rgb(44, 125, 144);
}
TitleBar #buttonClose:pressed {
    background-color: rgb(161, 73, 92);
}
"""


class Default:
    ICON_SIZE: int = 20
    PALETTE_WINDOW_COLOR: QColor = QColor(240, 240, 240)
    TITLE_HEIGHT: int = 35
    WINDOW_MARGINS: int = 7


class TitleBarButtonEnum(Enum):
    MINIMUM = "🗕"
    MAXIMUM = "🗖"
    NORMAL = "🗗"
    CLOSE = "🗙"
    PIN = "🖈"


class TitleBar(QWidget):
    # Сигнал минимизации окна
    aboutWindowMinimized = pyqtSignal()

    # Сигнал максимизации окна
    aboutWindowMaximized = pyqtSignal()

    # Сигнал возвращения нормального размера окна
    aboutWindowNormalized = pyqtSignal()

    # Сигнал закрытия окна
    aboutWindowClosed = pyqtSignal()

    # Сигнал изменения флага поверх всех окон
    aboutWindowPinned = pyqtSignal(bool)

    # Сигнал перемещения окна
    aboutWindowMovedDelta = pyqtSignal(QPoint)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Поддержка настройки фона qss
        self.setAttribute(Qt.WA_StyledBackground, True)

        self._old_pos: QPoint | None = None

        # Размер значка по умолчанию
        self.iconSize: int = Default.ICON_SIZE

        # Установите цвет фона по умолчанию, иначе он будет прозрачным из-за влияния родительского окна
        self.setAutoFillBackground(True)

        # TODO: Зачем оно нужно?
        palette = self.palette()
        palette.setColor(palette.Window, Default.PALETTE_WINDOW_COLOR)
        self.setPalette(palette)

        # Иконка окна
        self.iconLabel = QLabel()

        # Название окна
        self.titleLabel = ElidedLabel()
        self.titleLabel.setAlignment(Qt.AlignCenter)

        self.button_minimum = self.create_button(
            TitleBarButtonEnum.MINIMUM,
            on_clicked=self.aboutWindowMinimized.emit,
            object_name="buttonMinimum",
        )
        self.button_maximum = self.create_button(
            TitleBarButtonEnum.MAXIMUM,
            on_clicked=self.showMaximized,
            object_name="buttonMaximum",
        )
        self.button_close = self.create_button(
            TitleBarButtonEnum.CLOSE,
            on_clicked=self.aboutWindowClosed.emit,
            object_name="buttonClose",
        )

        self.button_pin = self.create_button(
            TitleBarButtonEnum.PIN,
            on_clicked=self.aboutWindowPinned.emit,
            object_name="buttonPin",
        )
        self.button_pin.setCheckable(True)
        self.button_pin.setChecked(False)

        self.layout_custom_widget = QHBoxLayout()
        self.layout_custom_widget.setContentsMargins(0, 0, 0, 0)

        main_layout = QHBoxLayout(self)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)

        main_layout.addSpacing(5)
        main_layout.addWidget(self.iconLabel)
        main_layout.addSpacing(5)

        main_layout.addWidget(self.titleLabel)
        main_layout.addSpacing(5)
        main_layout.addStretch()

        main_layout.addLayout(self.layout_custom_widget)

        main_layout.addSpacing(1)
        main_layout.addWidget(self.button_pin)
        main_layout.addSpacing(1)

        main_layout.addWidget(self.button_minimum)
        main_layout.addWidget(self.button_maximum)
        main_layout.addWidget(self.button_close)

        self.setHeight()

        self.setIcon(self.style().standardIcon(QStyle.SP_TitleBarMenuButton))

    def create_button(
        self,
        button_enum: TitleBarButtonEnum,
        on_clicked: callable,
        object_name: str,
    ) -> QToolButton:
        button = QToolButton()
        button.setObjectName(object_name)
        button.setText(button_enum.value)
        button.setAutoRaise(True)
        button.clicked.connect(on_clicked)

        return button

    def addWidget(
        self,
        widget: QWidget,
        width: int = Default.TITLE_HEIGHT,
        height: int = Default.TITLE_HEIGHT,
    ):
        self.layout_custom_widget.addWidget(widget)

        widget.setFixedSize(width, height)

    def showMaximized(self):
        if self.button_maximum.text() == TitleBarButtonEnum.MAXIMUM.value:
            # Максимизировать
            self.button_maximum.setText(TitleBarButtonEnum.NORMAL.value)
            self.aboutWindowMaximized.emit()
        else:  # Восстановить
            self.button_maximum.setText(TitleBarButtonEnum.MAXIMUM.value)
            self.aboutWindowNormalized.emit()

    def setHeight(self, height: int = Default.TITLE_HEIGHT):
        """Установка высоты строки заголовка"""

        self.setFixedHeight(height)

        for button in self.findChildren(QAbstractButton):
            button.setFixedSize(height, height)

    def setTitle(self, title: str):
        """Установить заголовок"""

        self.titleLabel.setText(title)

    def setIcon(self, icon: QIcon):
        """Настройки значкa"""

        self.iconLabel.setPixmap(icon.pixmap(self.iconSize, self.iconSize))

    def setIconSize(self, size: int):
        """Установить размер значка"""

        self.iconSize = size

    def enterEvent(self, _):
        self.setCursor(Qt.ArrowCursor)

    def mouseDoubleClickEvent(self, _):
        self.showMaximized()

    def mousePressEvent(self, event: QMouseEvent):
        """Событие клика мыши"""
        if event.button() == Qt.LeftButton:
            self._old_pos = event.pos()

        event.accept()

    def mouseReleaseEvent(self, event: QMouseEvent):
        """Событие отказов мыши"""
        self._old_pos = None
        event.accept()

    def mouseMoveEvent(self, event: QMouseEvent):
        if event.buttons() == Qt.LeftButton and self._old_pos:
            self.aboutWindowMovedDelta.emit(event.pos() - self._old_pos)

        event.accept()


# Перечислить верхнюю левую, нижнюю правую и четыре неподвижные точки
class DirectionEnum(Enum):
    LEFT = auto()
    TOP = auto()
    RIGHT = auto()
    BOTTOM = auto()

    LEFT_TOP = auto()
    RIGHT_TOP = auto()
    LEFT_BOTTOM = auto()
    RIGHT_BOTTOM = auto()


class FramelessWindow(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setStyleSheet(STYLE_SHEET)

        self._old_pos: QPoint | None = None
        self._direction: DirectionEnum | None = None

        self._widget: QWidget | None = None

        # Фон прозрачный
        self.setAttribute(Qt.WA_TranslucentBackground, True)

        # Нет границы
        self.setWindowFlag(Qt.FramelessWindowHint, True)

        # Отслеживание мыши
        self.setMouseTracking(True)

        # Панель заголовка
        self.titleBar = TitleBar(self)

        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(0)

        # Зарезервировать границы для изменения размера окна без полей
        main_layout.setContentsMargins(
            Default.WINDOW_MARGINS,
            Default.WINDOW_MARGINS,
            Default.WINDOW_MARGINS,
            Default.WINDOW_MARGINS,
        )
        main_layout.addWidget(self.titleBar)

        self.titleBar.aboutWindowMinimized.connect(self.showMinimized)
        self.titleBar.aboutWindowMaximized.connect(self.showMaximized)
        self.titleBar.aboutWindowNormalized.connect(self.showNormal)
        self.titleBar.aboutWindowClosed.connect(self.close)
        self.titleBar.aboutWindowPinned.connect(self.set_pinned)
        self.titleBar.aboutWindowMovedDelta.connect(self.delta_move)

        # TODO: Нужна синхронизация некоторых кнопок self.titleBar с состоянием окна, например
        #       поверх всех окон, во весь экран
        #       Например, сигнал для отправки флага окна? Или булевое значение?
        self.windowTitleChanged.connect(self.titleBar.setTitle)
        self.windowIconChanged.connect(self.titleBar.setIcon)

    def setTitleBarHeight(self, height: int = Default.TITLE_HEIGHT):
        """Установка высоты строки заголовка"""

        self.titleBar.setHeight(height)

    def setIconSize(self, size: int):
        """Установка размера значка"""

        self.titleBar.setIconSize(size)

    def setWidget(self, widget: QWidget):
        """Настройте свои собственные элементы управления"""

        self._widget = widget

        # Установите цвет фона по умолчанию, иначе он будет прозрачным из-за влияния родительского окна
        self._widget.setAutoFillBackground(True)
        palette = self._widget.palette()
        palette.setColor(palette.Window, Default.PALETTE_WINDOW_COLOR)
        self._widget.setPalette(palette)
        self._widget.installEventFilter(self)
        self.layout().addWidget(self._widget)

    def set_pinned(self, flag: bool):
        self.setWindowFlag(Qt.WindowStaysOnTopHint, flag)
        self.show()

    def delta_move(self, delta_pos: QPoint):
        if (
            self.windowState() == Qt.WindowMaximized
            or self.windowState() == Qt.WindowFullScreen
        ):
            # Максимизировать или полноэкранный режим не допускается
            return

        # Для перемещения окна
        self.move(self.pos() + delta_pos)

    def showMaximized(self):
        """
        Чтобы максимизировать, удалите верхнюю, нижнюю, левую и правую границы.
        Если вы не удалите его, в пограничной области будут пробелы.
        """

        super().showMaximized()

        self.layout().setContentsMargins(0, 0, 0, 0)

    def showNormal(self):
        """
        Восстановить, сохранить верхнюю и нижнюю левую и правую границы,
        иначе нет границы, которую нельзя отрегулировать
        """

        super().showNormal()

        self.layout().setContentsMargins(
            Default.WINDOW_MARGINS,
            Default.WINDOW_MARGINS,
            Default.WINDOW_MARGINS,
            Default.WINDOW_MARGINS,
        )

    def eventFilter(self, obj: QObject, event: QEvent):
        """
        Фильтр событий, используемый для решения мыши в других элементах
        управления и восстановления стандартного стиля мыши
        """

        if isinstance(event, QEnterEvent):
            self.setCursor(Qt.ArrowCursor)

        return super().eventFilter(obj, event)

    def paintEvent(self, event: QPaintEvent):
        """
        Поскольку это полностью прозрачное фоновое окно, жесткая для поиска
        граница с прозрачностью 1 рисуется в событии перерисовывания, чтобы отрегулировать размер окна.
        """

        super().paintEvent(event)

        # Физически окно больше на Default.WINDOW_MARGINS, добавление прозрачной рамки
        painter = QPainter(self)
        painter.setPen(
            QPen(
                QColor(255, 255, 255, 1),
                2 * Default.WINDOW_MARGINS,
            )
        )
        painter.drawRect(self.rect())

    def mousePressEvent(self, event: QMouseEvent):
        """Событие клика мыши"""

        super().mousePressEvent(event)

        if event.button() == Qt.LeftButton:
            self._old_pos = event.pos()

    def mouseReleaseEvent(self, event: QMouseEvent):
        """Событие отказов мыши"""

        super().mouseReleaseEvent(event)

        self._old_pos = None
        self._direction = None

    def mouseMoveEvent(self, event: QMouseEvent):
        """Событие перемещения мыши"""

        super().mouseMoveEvent(event)

        pos = event.pos()
        x_pos, y_pos = pos.x(), pos.y()
        wm, hm = (
            self.width() - Default.WINDOW_MARGINS,
            self.height() - Default.WINDOW_MARGINS,
        )

        if self.isMaximized() or self.isFullScreen():
            self._direction = None
            self.setCursor(Qt.ArrowCursor)
            return

        if event.buttons() == Qt.LeftButton and self._old_pos:
            self._resizeWidget(pos)
            return

        if x_pos <= Default.WINDOW_MARGINS and y_pos <= Default.WINDOW_MARGINS:
            # Верхний левый угол
            self._direction = DirectionEnum.LEFT_TOP
            self.setCursor(Qt.SizeFDiagCursor)

        elif wm <= x_pos <= self.width() and hm <= y_pos <= self.height():
            # Нижний правый угол
            self._direction = DirectionEnum.RIGHT_BOTTOM
            self.setCursor(Qt.SizeFDiagCursor)

        elif wm <= x_pos and y_pos <= Default.WINDOW_MARGINS:
            # верхний правый угол
            self._direction = DirectionEnum.RIGHT_TOP
            self.setCursor(Qt.SizeBDiagCursor)

        elif x_pos <= Default.WINDOW_MARGINS and hm <= y_pos:
            # Нижний левый угол
            self._direction = DirectionEnum.LEFT_BOTTOM
            self.setCursor(Qt.SizeBDiagCursor)

        elif 0 <= x_pos <= Default.WINDOW_MARGINS <= y_pos <= hm:
            # Влево
            self._direction = DirectionEnum.LEFT
            self.setCursor(Qt.SizeHorCursor)

        elif wm <= x_pos <= self.width() and Default.WINDOW_MARGINS <= y_pos <= hm:
            # Право
            self._direction = DirectionEnum.RIGHT
            self.setCursor(Qt.SizeHorCursor)

        elif wm >= x_pos >= Default.WINDOW_MARGINS >= y_pos >= 0:
            # выше
            self._direction = DirectionEnum.TOP
            self.setCursor(Qt.SizeVerCursor)

        elif Default.WINDOW_MARGINS <= x_pos <= wm and hm <= y_pos <= self.height():
            # ниже
            self._direction = DirectionEnum.BOTTOM
            self.setCursor(Qt.SizeVerCursor)

        else:
            # Курсор по умолчанию
            self.setCursor(Qt.ArrowCursor)

    def _resizeWidget(self, pos: QPoint):
        """Отрегулируйте размер окна"""

        if self._direction is None:
            return

        delta_pos = pos - self._old_pos
        x_pos, y_pos = delta_pos.x(), delta_pos.y()
        geometry = self.geometry()
        x, y, w, h = geometry.x(), geometry.y(), geometry.width(), geometry.height()

        if self._direction == DirectionEnum.LEFT_TOP:
            if w - x_pos > self.minimumWidth():
                x += x_pos
                w -= x_pos

            if h - y_pos > self.minimumHeight():
                y += y_pos
                h -= y_pos

        elif self._direction == DirectionEnum.RIGHT_BOTTOM:
            if w + x_pos > self.minimumWidth():
                w += x_pos
                self._old_pos = pos

            if h + y_pos > self.minimumHeight():
                h += y_pos
                self._old_pos = pos

        elif self._direction == DirectionEnum.RIGHT_TOP:
            if h - y_pos > self.minimumHeight():
                y += y_pos
                h -= y_pos

            if w + x_pos > self.minimumWidth():
                w += x_pos
                self._old_pos.setX(pos.x())

        elif self._direction == DirectionEnum.LEFT_BOTTOM:
            if w - x_pos > self.minimumWidth():
                x += x_pos
                w -= x_pos

            if h + y_pos > self.minimumHeight():
                h += y_pos
                self._old_pos.setY(pos.y())

        elif self._direction == DirectionEnum.LEFT:
            if w - x_pos > self.minimumWidth():
                x += x_pos
                w -= x_pos
            else:
                return

        elif self._direction == DirectionEnum.RIGHT:
            if w + x_pos > self.minimumWidth():
                w += x_pos
                self._old_pos = pos
            else:
                return

        elif self._direction == DirectionEnum.TOP:
            if h - y_pos > self.minimumHeight():
                y += y_pos
                h -= y_pos
            else:
                return

        elif self._direction == DirectionEnum.BOTTOM:
            if h + y_pos > self.minimumHeight():
                h += y_pos
                self._old_pos = pos
            else:
                return

        self.setGeometry(x, y, w, h)


if __name__ == "__main__":
    import sys
    import traceback

    from PyQt5.QtWidgets import QApplication, QTextEdit, QMessageBox

    def log_uncaught_exceptions(ex_cls, ex, tb):
        text = f"{ex_cls.__name__}: {ex}:\n"
        text += "".join(traceback.format_tb(tb))

        print(text)
        QMessageBox.critical(None, "Error", text)
        sys.exit(1)

    sys.excepthook = log_uncaught_exceptions


    app = QApplication(sys.argv)

    w = FramelessWindow()
    w.setWindowTitle(__file__)

    # Добавить свое окно
    w.setWidget(QTextEdit("Hello World!", w))
    w.resize(400, 400)
    w.show()

    sys.exit(app.exec_())
