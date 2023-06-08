#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from PyQt5.QtWidgets import QApplication, QGraphicsItem, QGraphicsSceneMouseEvent
from PyQt5.QtGui import QPainter, QFont, QFontMetrics, QPainterPath, QColor
from PyQt5.QtCore import Qt, QRectF, QPointF, QRect, QPoint, QSizeF
from PyQt5.QtChart import QChart, QChartView, QLineSeries


# SOURCE: https://doc-snapshots.qt.io/qt5-5.12/qtcharts-callout-callout-h.html
class Callout(QGraphicsItem):
    def __init__(self, chart: QChart, parent=None):
        super().__init__(parent)

        self.hide()

        self._chart = chart
        self._chart.scene().addItem(self)

        self._text = ""
        self._textRect = QRectF()
        self._rect = QRectF()
        self._anchor = QPointF()
        self._font = QFont()

    def setText(self, text: str):
        self._text = text
        metrics = QFontMetrics(self._font)
        self._textRect = QRectF(
            metrics.boundingRect(QRect(0, 0, 150, 150), Qt.AlignLeft, self._text)
        )
        self._textRect.translate(5, 5)
        self.prepareGeometryChange()
        self._rect = QRectF(self._textRect.adjusted(-5, -5, 5, 5))

    def setAnchor(self, point: QPointF):
        self._anchor = point

    def updateGeometry(self):
        self.prepareGeometryChange()
        self.setPos(self._chart.mapToPosition(self._anchor) + QPoint(10, -50))

        rect = self.sceneBoundingRect()

        # Correction position by top
        if rect.top() < 0:
            self.setY(0)

        # Correction position by right
        view_width = self._chart.rect().width()
        if rect.right() > view_width:
            rect.moveRight(view_width)
            self.setX(rect.x())

        # Correction position by bottom
        view_height = self._chart.rect().height()
        if rect.bottom() > view_height:
            rect.moveBottom(view_height)
            self.setY(rect.y())

    def boundingRect(self):
        anchor = self.mapFromParent(self._chart.mapToPosition(self._anchor))
        rect = QRectF()
        rect.setLeft(min(self._rect.left(), anchor.x()))
        rect.setRight(max(self._rect.right(), anchor.x()))
        rect.setTop(min(self._rect.top(), anchor.y()))
        rect.setBottom(max(self._rect.bottom(), anchor.y()))
        return rect

    def paint(self, painter: QPainter, option, widget=None):
        path = QPainterPath()
        path.addRoundedRect(self._rect, 5, 5)

        anchor = self.mapFromParent(self._chart.mapToPosition(self._anchor))
        if not self._rect.contains(anchor):
            point1 = QPointF()
            point2 = QPointF()

            # establish the position of the anchor point in relation to self._rect
            above = anchor.y() <= self._rect.top()
            aboveCenter = (
                anchor.y() > self._rect.top() and anchor.y() <= self._rect.center().y()
            )
            belowCenter = (
                anchor.y() > self._rect.center().y()
                and anchor.y() <= self._rect.bottom()
            )
            below = anchor.y() > self._rect.bottom()

            onLeft = anchor.x() <= self._rect.left()
            leftOfCenter = (
                anchor.x() > self._rect.left() and anchor.x() <= self._rect.center().x()
            )
            rightOfCenter = (
                anchor.x() > self._rect.center().x()
                and anchor.x() <= self._rect.right()
            )
            onRight = anchor.x() > self._rect.right()

            # get the nearest self._rect corner.
            x = (onRight + rightOfCenter) * self._rect.width()
            y = (below + belowCenter) * self._rect.height()
            cornerCase = (
                (above and onLeft)
                or (above and onRight)
                or (below and onLeft)
                or (below and onRight)
            )
            vertical = abs(anchor.x() - x) > abs(anchor.y() - y)

            x1 = (
                x
                + leftOfCenter * 10
                - rightOfCenter * 20
                + cornerCase * (not vertical) * (onLeft * 10 - onRight * 20)
            )
            y1 = (
                y
                + aboveCenter * 10
                - belowCenter * 20
                + cornerCase * vertical * (above * 10 - below * 20)
            )
            point1.setX(x1)
            point1.setY(y1)

            x2 = (
                x
                + leftOfCenter * 20
                - rightOfCenter * 10
                + cornerCase * (not vertical) * (onLeft * 20 - onRight * 10)
            )
            y2 = (
                y
                + aboveCenter * 20
                - belowCenter * 10
                + cornerCase * vertical * (above * 20 - below * 10)
            )
            point2.setX(x2)
            point2.setY(y2)

            path.moveTo(point1)
            path.lineTo(anchor)
            path.lineTo(point2)
            path = path.simplified()

        painter.setFont(self._font)
        painter.setBrush(QColor(255, 255, 255))
        painter.drawPath(path)
        painter.drawText(self._textRect, self._text)

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent):
        event.setAccepted(True)

    def mouseMoveEvent(self, event: QGraphicsSceneMouseEvent):
        if event.buttons() & Qt.LeftButton:
            self.setPos(
                self.mapToParent(event.pos() - event.buttonDownPos(Qt.LeftButton))
            )
            event.setAccepted(True)
        else:
            event.setAccepted(False)


class ChartViewToolTips(QChartView):
    def __init__(self):
        super().__init__()

        self.setRenderHint(QPainter.Antialiasing)

        self._tooltip = None
        self._callout_font_family = None
        self._callouts = []

    def clear_all_tooltips(self):
        if self._tooltip:
            self.scene().removeItem(self._tooltip)

        for x in self._callouts:
            self.scene().removeItem(x)

    def _add_Callout(self) -> Callout:
        callout = Callout(self.chart())

        if self._callout_font_family:
            callout._font.setFamily(self._callout_font_family)

        return callout

    def show_series_tooltip(self, point, state: bool):
        if not self.chart():
            return

        if not self._tooltip:
            self._tooltip = self._add_Callout()

        if state:
            self._tooltip.setText("X: {} \nY: {}".format(point.x(), point.y()))
            self._tooltip.setAnchor(point)
            self._tooltip.setZValue(11)
            self._tooltip.updateGeometry()
            self._tooltip.show()
        else:
            self._tooltip.hide()

    def keepCallout(self, point):
        if not self.chart() or not self._tooltip:
            return

        self._tooltip.setAnchor(point)
        self._callouts.append(self._tooltip)

        self._tooltip = self._add_Callout()

    def mouseReleaseEvent(self, event):
        if self.chart():
            pos = event.pos()
            point = self.chart().mapToValue(pos)
            self.keepCallout(point)

        super().mouseReleaseEvent(event)

    def resizeEvent(self, event):
        if self.scene():
            size = QSizeF(event.size())

            self.scene().setSceneRect(QRectF(QPoint(0, 0), size))
            self.chart().resize(size)

            for callout in self._callouts:
                callout.updateGeometry()

        super().resizeEvent(event)


class MainWindow(ChartViewToolTips):
    def __init__(self):
        super().__init__()

        series = QLineSeries()
        series.setPointsVisible(True)
        series.setPointLabelsVisible(True)
        series.setPointLabelsFormat("(@xPoint, @yPoint)")
        series.hovered.connect(self.show_series_tooltip)

        series.append(0, 6)
        series.append(2, 4)
        series.append(3, 8)
        series.append(7, 4)
        series.append(10, 5)

        self._chart = QChart()
        self._chart.setMinimumSize(640, 480)
        self._chart.setTitle("Line Chart Example")
        self._chart.setAnimationOptions(QChart.SeriesAnimations)
        self._chart.legend().hide()
        self._chart.addSeries(series)
        self._chart.createDefaultAxes()

        self.setChart(self._chart)


if __name__ == "__main__":
    app = QApplication([])

    mw = MainWindow()
    mw.setWindowTitle("Chart Line")
    mw.resize(800, 600)
    mw.show()

    app.exec()
