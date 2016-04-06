#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# TODO: from dev_window

# from PySide.QtWebKit import *
#
# QWebSettings.globalSettings().setAttribute(QWebSettings.DeveloperExtrasEnabled, True)
#
# self.view = QWebView()
# self.setCentralWidget(self.view)
#
# self.view.load('https://twitter.com/Misty_Shadow')
# self.doc = self.view.page().mainFrame().documentElement()
#
# def el_text(el, css_selector):
#     return el.findFirst(css_selector).toPlainText()
#
# profile = self.doc.findFirst('.ProfileHeaderCard')
#
# profile_info = {
#     'name': el_text(profile, '.ProfileHeaderCard-name'),
#     'screenname': el_text(profile, '.ProfileHeaderCard-screenname'),
#     'location': el_text(profile, '.ProfileHeaderCard-location'),
#     'url': el_text(profile, '.ProfileHeaderCard-url'),
#     'joinDate': el_text(profile, '.ProfileHeaderCard-joinDate'),
#     'birthdate': el_text(profile, '.ProfileHeaderCard-birthdate'),
# }
#
# text_mess = ''
#
# for k in sorted(profile_info.keys()):
#     text_mess += '{}: {}'.format(k, profile_info[k].strip()) + '\n'
#
# print(text_mess)
#
# QMessageBox.information(self, None, text_mess)