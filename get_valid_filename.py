#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import re


# SOURCE: https://github.com/django/django/blob/03dbdfd9bbbbd0b0172aad648c6bbe3f39541137/django/utils/text.py#L221
def get_valid_filename(s):
    """
    Return the given string converted to a string that can be used for a clean
    filename. Remove leading and trailing spaces; convert other spaces to
    underscores; and remove anything that is not an alphanumeric, dash,
    underscore, or dot.
    >>> get_valid_filename("john's portrait in 2004.jpg")
    'johns_portrait_in_2004.jpg'
    """
    s = str(s).strip().replace(" ", "_")
    return re.sub(r"(?u)[^-\w.]", "", s)


if __name__ == "__main__":
    text = get_valid_filename("john's portrait in 2004.jpg")
    print(text)
    assert text == "johns_portrait_in_2004.jpg"

    text = get_valid_filename("График по jira.xlsm")
    print(text)
    assert text == "График_по_jira.xlsm"

    text = get_valid_filename(
        "$@.'CPCSEA'2014-1203-RSDp. Performance Evaluation Form' Non-Executive. (Package'2014-1203-RSD. IPetrash'). v[2-06]r.docx"
    )
    print(text)
    assert (
        text
        == ".CPCSEA2014-1203-RSDp._Performance_Evaluation_Form_Non-Executive._Package2014-1203-RSD._IPetrash._v2-06r.docx"
    )
