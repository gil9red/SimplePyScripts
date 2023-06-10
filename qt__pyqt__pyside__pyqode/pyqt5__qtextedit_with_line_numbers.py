#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from PyQt5 import Qt


class LineNumberArea(Qt.QWidget):
    def __init__(self, editor):
        super().__init__(editor)

        self.editor = editor

    def sizeHint(self):
        return Qt.QSize(self.editor.line_number_area_width(), 0)

    def paintEvent(self, event):
        self.editor.line_number_area_paint_event(event)


class CodeEditor(Qt.QPlainTextEdit):
    def __init__(self):
        super().__init__()

        self.setStyleSheet(
            """
            font-family:'Consolas'; 
            color: #ccc; 
            font-size: 20px;
            background-color: #2b2b2b;
        """
        )
        self.highlight_color = Qt.QColor(Qt.Qt.darkGreen)

        self.line_number_area = LineNumberArea(self)

        self.blockCountChanged.connect(self.update_line_number_area_width)
        self.updateRequest.connect(self.update_line_number_area)
        self.cursorPositionChanged.connect(self.highlight_current_line)

        self.update_line_number_area_width()

    def line_number_area_width(self):
        digits = 1
        count = max(1, self.blockCount())
        while count >= 10:
            count /= 10
            digits += 1

        space = 3 + self.fontMetrics().width("9") * digits
        return space

    def update_line_number_area_width(self):
        self.setViewportMargins(self.line_number_area_width(), 0, 0, 0)

    def update_line_number_area(self, rect, dy):
        if dy:
            self.line_number_area.scroll(0, dy)
        else:
            self.line_number_area.update(
                0, rect.y(), self.line_number_area.width(), rect.height()
            )

        if rect.contains(self.viewport().rect()):
            self.update_line_number_area_width()

    def resizeEvent(self, event):
        super().resizeEvent(event)

        cr = self.contentsRect()
        self.line_number_area.setGeometry(
            Qt.QRect(cr.left(), cr.top(), self.line_number_area_width(), cr.height())
        )

    def line_number_area_paint_event(self, event):
        painter = Qt.QPainter(self.line_number_area)

        painter.fillRect(event.rect(), Qt.Qt.lightGray)

        block = self.firstVisibleBlock()
        block_number = block.blockNumber()
        top = self.blockBoundingGeometry(block).translated(self.contentOffset()).top()
        bottom = top + self.blockBoundingRect(block).height()

        height = self.fontMetrics().height()
        while block.isValid() and (top <= event.rect().bottom()):
            if block.isVisible() and (bottom >= event.rect().top()):
                number = str(block_number + 1)
                painter.setPen(Qt.Qt.black)
                painter.drawText(
                    0,
                    top,
                    self.line_number_area.width(),
                    height,
                    Qt.Qt.AlignRight,
                    number,
                )

            block = block.next()
            top = bottom
            bottom = top + self.blockBoundingRect(block).height()
            block_number += 1

    def highlight_current_line(self):
        extra_selections = []

        if not self.isReadOnly():
            line_color = self.highlight_color

            selection = Qt.QTextEdit.ExtraSelection()
            selection.format.setBackground(line_color)
            selection.format.setProperty(Qt.QTextFormat.FullWidthSelection, True)
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()
            extra_selections.append(selection)

        self.setExtraSelections(extra_selections)


if __name__ == "__main__":
    app = Qt.QApplication([])

    with open(__file__, encoding="utf-8") as f:
        text = f.read()

    code_editor = CodeEditor()
    code_editor.setPlainText(text)
    code_editor.setGeometry(400, 100, 600, 400)
    code_editor.show()

    app.exec()
