#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


"""
Скрипт, использую регулярные выражения, находит текст по шаблону и
заменяет его на аналогичный, но в верхнем регистре.
"""


import re


text = """
<xs:schema elementFormDefault="qualified" xmlns:xs="http://www.w3.org/2001/XMLSchema">
    <xs:element name="Root">
        <xs:complexType>
            <xs:sequence>
                <xs:element name="string_1">
                    <xs:complexType>
                        <xs:sequence>
                            <xs:element name="string_1_1" type="xs:string"/>
                            <xs:element name="string_1_2" type="xs:string"/>
                            <xs:element name="string_1_3" type="xs:string"/>
                        </xs:sequence>
                    </xs:complexType>
                </xs:element>

                <xs:element name="string" type="xs:string"/>
                <xs:element name="normalizedString" type="xs:normalizedString"/>
                <xs:element name="token" type="xs:token"/>
                <xs:element name="base64Binary" type="xs:base64Binary"/>
                <xs:element name="hexBinary" type="xs:hexBinary"/>
            </xs:sequence>
        </xs:complexType>
    </xs:element>
</xs:schema>
"""

text = re.sub('name="(.+?)"', lambda x: f'name="{x.group(1).upper()}"', text)
print(text)
