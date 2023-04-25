#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# pip install lxml
# pip install html5lib
# pip install bs4

from bs4 import BeautifulSoup


text = "<xml/>"

root = BeautifulSoup(text, "html.parser")
print(root.builder)  # bs4.builder._htmlparser.HTMLParserTreeBuilder

root = BeautifulSoup(text, "html5lib")
print(root.builder)  # bs4.builder._html5lib.HTML5TreeBuilder

root = BeautifulSoup(text, "xml")
print(root.builder)  # bs4.builder._lxml.LXMLTreeBuilderForXML

root = BeautifulSoup(text, "lxml-xml")
print(root.builder)  # bs4.builder._lxml.LXMLTreeBuilderForXML

root = BeautifulSoup(text, "lxml")
print(root.builder)  # bs4.builder._lxml.LXMLTreeBuilder

root = BeautifulSoup(text, "lxml-html")
print(root.builder)  # bs4.builder._lxml.LXMLTreeBuilder
