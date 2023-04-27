#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# pip install cssselect
from cssselect import HTMLTranslator


css_to_xpath = HTMLTranslator(xhtml=True).css_to_xpath


if __name__ == "__main__":
    xpath_expr = css_to_xpath("div#main > a[href]")
    print(xpath_expr)  # descendant-or-self::div[@id = 'main']/a[@href]

    xpath_expr = css_to_xpath("div")
    print(xpath_expr)  # descendant-or-self::div

    xpath_expr = css_to_xpath("table:nth-last-child(1)")
    print(xpath_expr)  # descendant-or-self::table[count(following-sibling::*) = 0]

    print()

    for item in (
        "#title",
        "#head",
        "#heading",
        ".pageTitle",
        ".news_title",
        ".title",
        ".head",
        ".heading",
        ".contentheading",
        ".small_header_red",
    ):
        xpath_expr = css_to_xpath(item)
        print(xpath_expr)
