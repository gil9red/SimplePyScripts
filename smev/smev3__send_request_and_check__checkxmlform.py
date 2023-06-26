#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import requests
from bs4 import BeautifulSoup


def send_check(xml_text):
    # Версия 1.2
    form_data = {
        "type": "checkxml",
        "schemaVersion": "20",
        "textarea-area": xml_text,
    }

    rs = requests.post("https://smev3.gosuslugi.ru/portal/checkxmlform", data=form_data)
    return rs.json()


RQ_ITEMS = [
    """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"><soapenv:Body><ns:SendRequestRequest xmlns:ns="urn://x-artefacts-smev-gov-ru/services/message-exchange/types/1.2"><ns:SenderProvidedRequestData Id="SIGNED_BY_CONSUMER"><ns:MessageID>cdbcea40-de9a-11e8-cee1-891cbddbaf49</ns:MessageID><ns:NodeID>181102449082753879</ns:NodeID><ns1:MessagePrimaryContent xmlns:ns1="urn://x-artefacts-smev-gov-ru/services/message-exchange/types/basic/1.2"><ns2:ExportChargesRequest xmlns:ns2="urn://roskazna.ru/gisgmp/xsd/services/export-charges/2.0.1" Id="ID_181102449082753879" senderIdentifier="30108f" senderRole="7" timestamp="2018-11-02T17:28:29.165+05:00"><ns3:ChargesExportConditions xmlns:ns3="http://roskazna.ru/gisgmp/xsd/SearchConditions/2.0.1" kind="CHARGE"><ns3:ChargesConditions><ns3:SupplierBillID>123</ns3:SupplierBillID></ns3:ChargesConditions></ns3:ChargesExportConditions></ns2:ExportChargesRequest></ns1:MessagePrimaryContent><ns:TestMessage/></ns:SenderProvidedRequestData><ns:CallerInformationSystemSignature><ds:Signature xmlns:ds="http://www.w3.org/2000/09/xmldsig#"><ds:SignedInfo><ds:CanonicalizationMethod Algorithm="http://www.w3.org/2001/10/xml-exc-c14n#"/><ds:SignatureMethod Algorithm="http://www.w3.org/2001/04/xmldsig-more#gostr34102001-gostr3411"/><ds:Reference URI="#SIGNED_BY_CONSUMER"><ds:Transforms><ds:Transform Algorithm="http://www.w3.org/2001/10/xml-exc-c14n#"/><ds:Transform Algorithm="urn://smev-gov-ru/xmldsig/transform"/></ds:Transforms><ds:DigestMethod Algorithm="http://www.w3.org/2001/04/xmldsig-more#gostr3411"/><ds:DigestValue>PxEU16mOjiIhcrm8+G0JM9/t40hTJDnIVdzYkf1IuX4=</ds:DigestValue></ds:Reference></ds:SignedInfo><ds:SignatureValue>4N4g59gH4vQ5EZFuT3kw6iIkQXyHqy1XpzjGtL+laadJl+yo2QFSkRB25QKmGHsEZRZ2gWHbh/i8iUg6knqGPw==</ds:SignatureValue><ds:KeyInfo><ds:X509Data><ds:X509Certificate>MIIBjzCCAT6gAwIBAgIFAK0bIlkwCAYGKoUDAgIDMDExCzAJBgNVBAYTAlJVMRIwEAYDVQQKDAlDcnlwdG9Qcm8xDjAMBgNVBAMMBUFsaWFzMB4XDTE4MDkyNTEyMTgwMFoXDTE5MDkyNTEyMTgwMFowMTELMAkGA1UEBhMCUlUxEjAQBgNVBAoMCUNyeXB0b1BybzEOMAwGA1UEAwwFQWxpYXMwYzAcBgYqhQMCAhMwEgYHKoUDAgIkAAYHKoUDAgIeAQNDAARA1/RkKouLLrgR33bZYmaJslhiYtsEuaEcn4VV/w8f8nI7RZpIkKt+AIOYiIrmP1/DSjvmSgw17Jwt/oI3DdGvhaM7MDkwDgYDVR0PAQH/BAQDAgPoMBMGA1UdJQQMMAoGCCsGAQUFBwMCMBIGA1UdEwEB/wQIMAYBAf8CAQUwCAYGKoUDAgIDA0EA81lwsJ/jkOSXBp06HYDQL95pBNgrWDaODEq6sdnB8CFPg0VoDbNzI1m/YGaTdBpz8IvYJUjXIYv+28Kw+7Py1w==</ds:X509Certificate></ds:X509Data></ds:KeyInfo></ds:Signature></ns:CallerInformationSystemSignature></ns:SendRequestRequest></soapenv:Body></soapenv:Envelope>""",
    """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"><soapenv:Body><ns:SendRequestRequest xmlns:ns="urn://x-artefacts-smev-gov-ru/services/message-exchange/types/1.2"><ns:SenderProvidedRequestData Id="SIGNED_BY_CONSUMER"><ns:MessageID>a43bca90-de97-11e8-2d5c-4bd96a9f1e4e</ns:MessageID><ns:NodeID>181102435491653853</ns:NodeID><ns1:MessagePrimaryContent xmlns:ns1="urn://x-artefacts-smev-gov-ru/services/message-exchange/types/basic/1.2"><ns2:ImportPaymentsRequest xmlns:ns2="urn://roskazna.ru/gisgmp/xsd/services/import-payments/2.0.1" Id="ID_181102435491653853" senderIdentifier="30108f" senderRole="7" timestamp="2018-11-02T17:05:50.401+05:00"><ns3:PaymentsPackage xmlns:ns3="http://roskazna.ru/gisgmp/xsd/Package/2.0.1"><ns3:ImportedPayment Id="ID_63RZ77DX7ZEOJP34H3D5JTNPDE" amount="0" kbk="32111301030016000130" oktmo="45348000" paymentDate="2018-11-02+05:00" paymentId="10000000000000000211201891653853" purpose="Плата за предоставление информации о зарегистрированных правах на недвижимое имущество и сделок с ним" receiptDate="2018-11-02+05:00" supplierBillID="32117072411021588933" transKind="01"><ns4:PaymentOrg xmlns:ns4="http://roskazna.ru/gisgmp/xsd/Payment/2.0.1"><ns5:Bank xmlns:ns5="http://roskazna.ru/gisgmp/xsd/Organization/2.0.1" bik="000000000"/></ns4:PaymentOrg><ns4:Payer xmlns:ns4="http://roskazna.ru/gisgmp/xsd/Payment/2.0.1" payerIdentifier="1010000000008751379232"/><ns4:Payee xmlns:ns4="http://roskazna.ru/gisgmp/xsd/Organization/2.0.1" inn="7705401341" kpp="770542151" name="ФГБУ «ФКП Росреестра» по г Москва"><ns5:OrgAccount xmlns:ns5="http://roskazna.ru/gisgmp/xsd/Common/2.0.1" accountNumber="40101200500000010041"><ns5:Bank bik="047102001"/></ns5:OrgAccount></ns4:Payee><ns4:BudgetIndex xmlns:ns4="http://roskazna.ru/gisgmp/xsd/Payment/2.0.1" paytReason="0" status="01" taxDocDate="0" taxDocNumber="0" taxPeriod="0"/><ns4:AccDoc xmlns:ns4="http://roskazna.ru/gisgmp/xsd/Payment/2.0.1" accDocDate="2018-11-02+05:00"/><ns4:ChangeStatus xmlns:ns4="http://roskazna.ru/gisgmp/xsd/Common/2.0.1" meaning="1"/></ns3:ImportedPayment></ns3:PaymentsPackage></ns2:ImportPaymentsRequest></ns1:MessagePrimaryContent><ns:TestMessage/></ns:SenderProvidedRequestData><ns:CallerInformationSystemSignature><ds:Signature xmlns:ds="http://www.w3.org/2000/09/xmldsig#"><ds:SignedInfo><ds:CanonicalizationMethod Algorithm="http://www.w3.org/2001/10/xml-exc-c14n#"/><ds:SignatureMethod Algorithm="http://www.w3.org/2001/04/xmldsig-more#gostr34102001-gostr3411"/><ds:Reference URI="#SIGNED_BY_CONSUMER"><ds:Transforms><ds:Transform Algorithm="http://www.w3.org/2001/10/xml-exc-c14n#"/><ds:Transform Algorithm="urn://smev-gov-ru/xmldsig/transform"/></ds:Transforms><ds:DigestMethod Algorithm="http://www.w3.org/2001/04/xmldsig-more#gostr3411"/><ds:DigestValue>ezp+FwkUu4vR28BwFZFDNdAJjGQEcx4nlwC8QWaRCN8=</ds:DigestValue></ds:Reference></ds:SignedInfo><ds:SignatureValue>JkzKVa49yD2wOsWD/KXMAh3D7r9tdYOu4QcXqjW3dTKNOMUdZpLZcKY9QBA+uVbK0iuI3VoRwKlZS9Qhoa3mvQ==</ds:SignatureValue><ds:KeyInfo><ds:X509Data><ds:X509Certificate>MIIBjzCCAT6gAwIBAgIFAK0bIlkwCAYGKoUDAgIDMDExCzAJBgNVBAYTAlJVMRIwEAYDVQQKDAlDcnlwdG9Qcm8xDjAMBgNVBAMMBUFsaWFzMB4XDTE4MDkyNTEyMTgwMFoXDTE5MDkyNTEyMTgwMFowMTELMAkGA1UEBhMCUlUxEjAQBgNVBAoMCUNyeXB0b1BybzEOMAwGA1UEAwwFQWxpYXMwYzAcBgYqhQMCAhMwEgYHKoUDAgIkAAYHKoUDAgIeAQNDAARA1/RkKouLLrgR33bZYmaJslhiYtsEuaEcn4VV/w8f8nI7RZpIkKt+AIOYiIrmP1/DSjvmSgw17Jwt/oI3DdGvhaM7MDkwDgYDVR0PAQH/BAQDAgPoMBMGA1UdJQQMMAoGCCsGAQUFBwMCMBIGA1UdEwEB/wQIMAYBAf8CAQUwCAYGKoUDAgIDA0EA81lwsJ/jkOSXBp06HYDQL95pBNgrWDaODEq6sdnB8CFPg0VoDbNzI1m/YGaTdBpz8IvYJUjXIYv+28Kw+7Py1w==</ds:X509Certificate></ds:X509Data></ds:KeyInfo></ds:Signature></ns:CallerInformationSystemSignature></ns:SendRequestRequest></soapenv:Body></soapenv:Envelope>""",
]
URL = "http://smev3-n0.test.gosuslugi.ru:7500/smev/v1.2/ws?wsdl"
HEADERS = {
    "SOAPAction": "urn:SendRequest",
    # Без этого заголовка запрос с кириллицей не проходил проверку электронной подписи
    # Запрос удачно пройдет и с "text/xml;charset=utf-8"
    "Content-Type": "application/xml;charset=utf-8",
}

for rq in RQ_ITEMS:
    rs = requests.post(URL, bytes(rq, encoding="utf-8"), headers=HEADERS)
    print(rs, rs.content)
    root = BeautifulSoup(rs.content, "html.parser")
    faultstring = root.select_one("faultstring")
    print("faultstring", faultstring)
    print(send_check(rq))

    print()
