# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created: Thu Mar 10 11:02:45 2016
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(831, 573)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setObjectName("formLayout")
        self.label_4 = QtGui.QLabel(self.centralwidget)
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label_4)
        self.url = QtGui.QLabel(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(
            QtGui.QSizePolicy.Ignored, QtGui.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.url.sizePolicy().hasHeightForWidth())
        self.url.setSizePolicy(sizePolicy)
        self.url.setWordWrap(True)
        self.url.setOpenExternalLinks(True)
        self.url.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse)
        self.url.setObjectName("url")
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.url)
        self.verticalLayout_3.addLayout(self.formLayout)
        self.splitter = QtGui.QSplitter(self.centralwidget)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName("splitter")
        self.widget = QtGui.QWidget(self.splitter)
        self.widget.setObjectName("widget")
        self.verticalLayout = QtGui.QVBoxLayout(self.widget)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_6 = QtGui.QLabel(self.widget)
        self.label_6.setObjectName("label_6")
        self.verticalLayout.addWidget(self.label_6)
        self.ref_guide = QtGui.QPlainTextEdit(self.widget)
        self.ref_guide.setObjectName("ref_guide")
        self.verticalLayout.addWidget(self.ref_guide)
        self.widget_2 = QtGui.QWidget(self.splitter)
        self.widget_2.setObjectName("widget_2")
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.widget_2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_7 = QtGui.QLabel(self.widget_2)
        self.label_7.setObjectName("label_7")
        self.verticalLayout_2.addWidget(self.label_7)
        self.description = QtGui.QPlainTextEdit(self.widget_2)
        self.description.setObjectName("description")
        self.verticalLayout_2.addWidget(self.description)
        self.verticalLayout_3.addWidget(self.splitter)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 831, 21))
        self.menubar.setObjectName("menubar")
        self.menuDockWindow = QtGui.QMenu(self.menubar)
        self.menuDockWindow.setObjectName("menuDockWindow")
        self.menuTools = QtGui.QMenu(self.menubar)
        self.menuTools.setObjectName("menuTools")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolBarGeneral = QtGui.QToolBar(MainWindow)
        self.toolBarGeneral.setObjectName("toolBarGeneral")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBarGeneral)
        self.dock_widget_tag_list = QtGui.QDockWidget(MainWindow)
        self.dock_widget_tag_list.setObjectName("dock_widget_tag_list")
        self.dockWidgetContents = QtGui.QWidget()
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.dockWidgetContents)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.check_box_only_empty = QtGui.QCheckBox(self.dockWidgetContents)
        self.check_box_only_empty.setObjectName("check_box_only_empty")
        self.verticalLayout_4.addWidget(self.check_box_only_empty)
        self.list_view_tag_list = QtGui.QListView(self.dockWidgetContents)
        self.list_view_tag_list.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.list_view_tag_list.setObjectName("list_view_tag_list")
        self.verticalLayout_4.addWidget(self.list_view_tag_list)
        self.dock_widget_tag_list.setWidget(self.dockWidgetContents)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(1), self.dock_widget_tag_list)
        self.dock_widget_modified_tags = QtGui.QDockWidget(MainWindow)
        self.dock_widget_modified_tags.setObjectName("dock_widget_modified_tags")
        self.dockWidgetContents_2 = QtGui.QWidget()
        self.dockWidgetContents_2.setObjectName("dockWidgetContents_2")
        self.verticalLayout_5 = QtGui.QVBoxLayout(self.dockWidgetContents_2)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.list_view_modified_tags = QtGui.QListView(self.dockWidgetContents_2)
        self.list_view_modified_tags.setEditTriggers(
            QtGui.QAbstractItemView.NoEditTriggers
        )
        self.list_view_modified_tags.setObjectName("list_view_modified_tags")
        self.verticalLayout_5.addWidget(self.list_view_modified_tags)
        self.dock_widget_modified_tags.setWidget(self.dockWidgetContents_2)
        MainWindow.addDockWidget(
            QtCore.Qt.DockWidgetArea(2), self.dock_widget_modified_tags
        )
        self.dock_widget_tag_info = QtGui.QDockWidget(MainWindow)
        self.dock_widget_tag_info.setObjectName("dock_widget_tag_info")
        self.dockWidgetContents_4 = QtGui.QWidget()
        self.dockWidgetContents_4.setObjectName("dockWidgetContents_4")
        self.verticalLayout_6 = QtGui.QVBoxLayout(self.dockWidgetContents_4)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.plain_text_edit_tag_info = QtGui.QPlainTextEdit(self.dockWidgetContents_4)
        self.plain_text_edit_tag_info.setReadOnly(True)
        self.plain_text_edit_tag_info.setObjectName("plain_text_edit_tag_info")
        self.verticalLayout_6.addWidget(self.plain_text_edit_tag_info)
        self.dock_widget_tag_info.setWidget(self.dockWidgetContents_4)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(2), self.dock_widget_tag_info)
        self.action_save = QtGui.QAction(MainWindow)
        self.action_save.setObjectName("action_save")
        self.action_save_all = QtGui.QAction(MainWindow)
        self.action_save_all.setObjectName("action_save_all")
        self.menubar.addAction(self.menuDockWindow.menuAction())
        self.menubar.addAction(self.menuTools.menuAction())
        self.toolBarGeneral.addAction(self.action_save)
        self.toolBarGeneral.addAction(self.action_save_all)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        self.label_4.setText(
            QtGui.QApplication.translate(
                "MainWindow", "Url:", None, QtGui.QApplication.UnicodeUTF8
            )
        )
        self.url.setText(
            QtGui.QApplication.translate(
                "MainWindow", "<tag_url>", None, QtGui.QApplication.UnicodeUTF8
            )
        )
        self.label_6.setText(
            QtGui.QApplication.translate(
                "MainWindow", "Reference guide:", None, QtGui.QApplication.UnicodeUTF8
            )
        )
        self.label_7.setText(
            QtGui.QApplication.translate(
                "MainWindow", "Description:", None, QtGui.QApplication.UnicodeUTF8
            )
        )
        self.menuDockWindow.setTitle(
            QtGui.QApplication.translate(
                "MainWindow", "Окна", None, QtGui.QApplication.UnicodeUTF8
            )
        )
        self.menuTools.setTitle(
            QtGui.QApplication.translate(
                "MainWindow", "Tools", None, QtGui.QApplication.UnicodeUTF8
            )
        )
        self.toolBarGeneral.setWindowTitle(
            QtGui.QApplication.translate(
                "MainWindow", "General", None, QtGui.QApplication.UnicodeUTF8
            )
        )
        self.dock_widget_tag_list.setWindowTitle(
            QtGui.QApplication.translate(
                "MainWindow", "Tag list", None, QtGui.QApplication.UnicodeUTF8
            )
        )
        self.check_box_only_empty.setText(
            QtGui.QApplication.translate(
                "MainWindow", "Only empty tags", None, QtGui.QApplication.UnicodeUTF8
            )
        )
        self.dock_widget_modified_tags.setWindowTitle(
            QtGui.QApplication.translate(
                "MainWindow", "Modified tags", None, QtGui.QApplication.UnicodeUTF8
            )
        )
        self.dock_widget_tag_info.setWindowTitle(
            QtGui.QApplication.translate(
                "MainWindow", "Tag info", None, QtGui.QApplication.UnicodeUTF8
            )
        )
        self.action_save.setText(
            QtGui.QApplication.translate(
                "MainWindow", "Save", None, QtGui.QApplication.UnicodeUTF8
            )
        )
        self.action_save_all.setText(
            QtGui.QApplication.translate(
                "MainWindow", "Save All", None, QtGui.QApplication.UnicodeUTF8
            )
        )
        self.action_save_all.setToolTip(
            QtGui.QApplication.translate(
                "MainWindow", "Save All Tags", None, QtGui.QApplication.UnicodeUTF8
            )
        )
