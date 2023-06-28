#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import xml.dom.minidom
from datetime import datetime


# SOURCE: https://ru.stackoverflow.com/questions/905565/
text = """\
<Response>
    <Data>
        <Report>
            <LeaderList>
                <Leader ActualDate="2009-12-01" FIO="Шxxxxxxx Аxxxxx Шxxxxxx" INN="5xxxxxxxxx" Position="генеральный директор"/>
                <Leader ActualDate="2008-10-07" FIO="Вxxxxxx Аxxxxxx Аxxxxxxx" Position="генеральный директор"/>
                <Leader ActualDate="2007-04-17" FIO="Оxxxxxxxx Сxxxxx Вxxxxxxx" Position="генеральный директор"/>
                <Leader ActualDate="2004-12-06" FIO="Кxxxxxxx Аxxxxxxx Нxxxxxx" Position="генеральный директор"/>
            </LeaderList>
        </Report>
    </Data>
    <ResultInfo ExecutionTime="140" ResultType="True"/>
</Response>
"""


def to_date(date_str):
    return datetime.strptime(date_str, "%Y-%m-%d")


dom = xml.dom.minidom.parseString(text)
items = dom.getElementsByTagName("Leader")
leader = max(items, key=lambda x: to_date(x.attributes["ActualDate"].value))

print(leader.attributes["FIO"].value)  # Шxxxxxxx Аxxxxx Шxxxxxx
print(leader.attributes["ActualDate"].value)  # 2009-12-01
print(leader.attributes["Position"].value)  # генеральный директор
