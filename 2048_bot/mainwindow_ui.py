# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(864, 692)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 864, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuDockWindow = QtGui.QMenu(self.menubar)
        self.menuDockWindow.setObjectName(_fromUtf8("menuDockWindow"))
        self.menuTools = QtGui.QMenu(self.menubar)
        self.menuTools.setObjectName(_fromUtf8("menuTools"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.dock_widget_exec = QtGui.QDockWidget(MainWindow)
        self.dock_widget_exec.setObjectName(_fromUtf8("dock_widget_exec"))
        self.dock_widget_exec_contents = QtGui.QWidget()
        self.dock_widget_exec_contents.setObjectName(_fromUtf8("dock_widget_exec_contents"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.dock_widget_exec_contents)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.button_exec = QtGui.QPushButton(self.dock_widget_exec_contents)
        self.button_exec.setObjectName(_fromUtf8("button_exec"))
        self.verticalLayout_2.addWidget(self.button_exec)
        self.container_code_editor = QtGui.QScrollArea(self.dock_widget_exec_contents)
        self.container_code_editor.setFrameShape(QtGui.QFrame.NoFrame)
        self.container_code_editor.setWidgetResizable(True)
        self.container_code_editor.setObjectName(_fromUtf8("container_code_editor"))
        self.scrollAreaWidgetContents = QtGui.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 256, 160))
        self.scrollAreaWidgetContents.setObjectName(_fromUtf8("scrollAreaWidgetContents"))
        self.container_code_editor.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout_2.addWidget(self.container_code_editor)
        self.dock_widget_exec.setWidget(self.dock_widget_exec_contents)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(2), self.dock_widget_exec)
        self.dock_widget_simple_log = QtGui.QDockWidget(MainWindow)
        self.dock_widget_simple_log.setObjectName(_fromUtf8("dock_widget_simple_log"))
        self.dockWidgetContents = QtGui.QWidget()
        self.dockWidgetContents.setObjectName(_fromUtf8("dockWidgetContents"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.dockWidgetContents)
        self.verticalLayout_3.setContentsMargins(-1, 2, -1, -1)
        self.verticalLayout_3.setSpacing(2)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.button_clear_slog = QtGui.QToolButton(self.dockWidgetContents)
        self.button_clear_slog.setObjectName(_fromUtf8("button_clear_slog"))
        self.verticalLayout_3.addWidget(self.button_clear_slog)
        self.simple_log = QtGui.QPlainTextEdit(self.dockWidgetContents)
        self.simple_log.setObjectName(_fromUtf8("simple_log"))
        self.verticalLayout_3.addWidget(self.simple_log)
        self.dock_widget_simple_log.setWidget(self.dockWidgetContents)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(2), self.dock_widget_simple_log)
        self.toolBarGeneral = QtGui.QToolBar(MainWindow)
        self.toolBarGeneral.setObjectName(_fromUtf8("toolBarGeneral"))
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBarGeneral)
        self.dock_widget_output = QtGui.QDockWidget(MainWindow)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dock_widget_output.sizePolicy().hasHeightForWidth())
        self.dock_widget_output.setSizePolicy(sizePolicy)
        self.dock_widget_output.setObjectName(_fromUtf8("dock_widget_output"))
        self.dockWidgetContents_3 = QtGui.QWidget()
        self.dockWidgetContents_3.setObjectName(_fromUtf8("dockWidgetContents_3"))
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.dockWidgetContents_3)
        self.verticalLayout_4.setContentsMargins(-1, 2, -1, -1)
        self.verticalLayout_4.setSpacing(2)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.button_clear_output = QtGui.QToolButton(self.dockWidgetContents_3)
        self.button_clear_output.setObjectName(_fromUtf8("button_clear_output"))
        self.verticalLayout_4.addWidget(self.button_clear_output)
        self.output = QtGui.QTextEdit(self.dockWidgetContents_3)
        self.output.setReadOnly(True)
        self.output.setObjectName(_fromUtf8("output"))
        self.verticalLayout_4.addWidget(self.output)
        self.dock_widget_output.setWidget(self.dockWidgetContents_3)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(8), self.dock_widget_output)
        self.menubar.addAction(self.menuDockWindow.menuAction())
        self.menubar.addAction(self.menuTools.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QObject.connect(self.button_clear_slog, QtCore.SIGNAL(_fromUtf8("clicked()")), self.simple_log.clear)
        QtCore.QObject.connect(self.button_clear_output, QtCore.SIGNAL(_fromUtf8("clicked()")), self.output.clear)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        self.menuDockWindow.setTitle(_translate("MainWindow", "Окна", None))
        self.menuTools.setTitle(_translate("MainWindow", "Tools", None))
        self.dock_widget_exec.setWindowTitle(_translate("MainWindow", "Выполнение скрипта", None))
        self.button_exec.setText(_translate("MainWindow", "Выполнить", None))
        self.button_exec.setShortcut(_translate("MainWindow", "Ctrl+Return", None))
        self.dock_widget_simple_log.setWindowTitle(_translate("MainWindow", "Простой лог", None))
        self.button_clear_slog.setToolTip(_translate("MainWindow", "Очистить лог", None))
        self.button_clear_slog.setStatusTip(_translate("MainWindow", "Очистить лог", None))
        self.button_clear_slog.setText(_translate("MainWindow", "Очистить", None))
        self.toolBarGeneral.setWindowTitle(_translate("MainWindow", "General", None))
        self.dock_widget_output.setWindowTitle(_translate("MainWindow", "Вывод", None))
        self.button_clear_output.setText(_translate("MainWindow", "Очистить", None))

