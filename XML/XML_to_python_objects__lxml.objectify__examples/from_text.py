#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://lxml.de/objectify.html


from datetime import datetime

# pip install lxml
from lxml import objectify


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


root = objectify.fromstring(text)
items = root.Data.Report.LeaderList.Leader

leader = max(items, key=lambda x: to_date(x.attrib["ActualDate"]))
print(leader.attrib["FIO"])  # Шxxxxxxx Аxxxxx Шxxxxxx
print(leader.attrib["ActualDate"])  # 2009-12-01
print(leader.attrib["Position"])  # генеральный директор
