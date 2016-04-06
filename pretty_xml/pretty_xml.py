#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


def process_xml_string(xml_string):
    """
    Функция из текста выдирает строку с xml --
    она должна начинаться на < и заканчиваться >

    """

    start = xml_string.index('<')
    end = xml_string.rindex('>')
    return xml_string[start:end + 1]


def pretty_xml_minidom(xml_string, ind=2):
    """Функция принимает строку xml и выводит xml с отступами."""

    from xml.dom.minidom import parseString

    xml_string = process_xml_string(xml_string)
    xml_utf8 = parseString(xml_string).toprettyxml(indent=' ' * ind, encoding='utf-8')
    return xml_utf8.decode('utf-8')


def pretty_xml_lxml(xml_string):
    """Функция принимает строку xml и выводит xml с отступами."""

    from lxml import etree

    xml_string = process_xml_string(xml_string)
    root = etree.fromstring(xml_string)
    return etree.tostring(root, pretty_print=True, encoding='utf-8').decode('utf-8')


if __name__ == '__main__':
    xml = '<a><b/><c><z/><h/></c></a>'
    print(pretty_xml_minidom(xml))
    print(pretty_xml_lxml(xml))



# #!/usr/bin/env python3
# # -*- coding: utf-8 -*-
#
#
# __author__ = 'ipetrash'
#
#
# # from PySide.QtGui import *
# # import xml.dom.minidom
# # import sys
# #
# #
# # class Window(QWidget):
# #     def __init__(self):
# #         super().__init__()
# #
# #         self.input = QPlainTextEdit()
# #         self.output = QPlainTextEdit()
# #
# #         splitter = QSplitter()
# #         splitter.addWidget(self.input)
# #         splitter.addWidget(self.output)
# #
# #         layout = QVBoxLayout()
# #         layout.addWidget(splitter)
# #
# #         self.setLayout(layout)
# #
# #
# # if __name__ == '__main__':
# #     app = QApplication
# #
# #
# #     xml_string = """
# #     <OperationRq Operation="CashDeposit" Rrn="150716001875" SurchargeCalculation="true" PinKeyId="1037045" Language="ru"><Parties xmlns="http://schemas.tranzaxis.com/sstp.xsd"><Cust Kind="Card"><Card Pan="4375620000000104" Track2="4375620000000104=1405101111111111111" EntryMode="Fallback" xmlns="http://schemas.tranzaxis.com/tran-common.xsd"><Auth Presence="true" PinBlock="D49FAA4F83BAE424" SignChecked="false" PhotoChecked="false" /></Card></Cust></Parties><Money Amt="200" Ccy="RUR" xmlns="http://schemas.tranzaxis.com/sstp.xsd"><Surcharges /></Money><Specific xmlns="http://schemas.tranzaxis.com/sstp.xsd"><CustInfo Kinds="ContractLedgerBalance ContractAvailBalance ContractCcyAc ContractRid ContractRespText ContractTranFeeAmt ContractTranCcyAc ContractPayeeTitle ContractPayeeRid" Language="ru" /><CashDenoms><Denom DeviceKind="ACCEPTOR" Ccy="810" Denomination="100" Cnt="2" xmlns="http://schemas.tranzaxis.com/tran-common.xsd" /><Denom DeviceKind="Acceptor" Ccy="RUR" Denom="100" Cnt="2" /></CashDenoms></Specific><Refines RefinedTranId="150716000002908596" xmlns="http://schemas.tranzaxis.com/sstp.xsd"><RefineRs Kind="CustomerContract" Value="00111444633719" /></Refines><UserAttrs xmlns="http://schemas.tranzaxis.com/sstp.xsd"><ParamValue Rid="TXSST_VERSION" xmlns="http://schemas.tranzaxis.com/common-types.xsd"><Val>0.2.91.1822.dev</Val></ParamValue></UserAttrs></OperationRq>
# #     """
# #
# #     xml = xml.dom.minidom.parseString(xml_string)
# #     pretty_xml_as_string = xml.toprettyxml()
# #     print(pretty_xml_as_string)
#
#
# import xml.dom.minidom
#
# xml_string = """
#
# <club>
#  <players>
#  <player id="kramnik"
#  name="Vladimir Kramnik"
#  rating="2700"
#  status="GM" />
#  <player id="fritz"
#  name="Deep Fritz"
#  rating="2700"
#  status="Computer" />
#  <player id="mertz"
#  name="David Mertz"
#  rating="1400"
#  status="Amateur" />
#  </players>
#  <matches>
#  <match>
#  <Date>2002-10-04</Date>
#  <White refid="fritz" />
#  <Black refid="kramnik" />
#  <Result>Draw</Result>
#  </match>
#  <match>
#  <Date>2002-10-06</Date>
#  <White refid="kramnik" />
#  <Black refid="fritz" />
#  <Result>White</Result>
#  </match>
#  </matches>
#  </club>
#
# """
#
#
# start = xml_string.index('<')
# end = xml_string.rindex('>')
# xml_string = xml_string[start:end + 1]
#
# # TODO: избавляемся от &lt; &gt; и т.п.
# # import html
# # xml_string = html.unescape(xml_string)
#
#
# xml = xml.dom.minidom.parseString(xml_string)
# pretty_xml_as_string = xml.toprettyxml()
#
# print(pretty_xml_as_string)
