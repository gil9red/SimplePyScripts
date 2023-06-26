#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# URL:  https://smev3.gosuslugi.ru/portal/checkxmlform.jsp
# AJAX: https://smev3.gosuslugi.ru/portal/checkxmlform


import requests


xml_text = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"><soapenv:Body><ns:AckRequest xmlns:ns="urn://x-artefacts-smev-gov-ru/services/message-exchange/types/1.2"><ns1:AckTargetMessage xmlns:ns1="urn://x-artefacts-smev-gov-ru/services/message-exchange/types/basic/1.2" Id="SIGNED_BY_CALLER" accepted="true">91686b40-af89-11e8-b8b3-005056857a87</ns1:AckTargetMessage><ns:CallerInformationSystemSignature><ds:Signature xmlns:ds="http://www.w3.org/2000/09/xmldsig#"><ds:SignedInfo><ds:CanonicalizationMethod Algorithm="http://www.w3.org/2001/10/xml-exc-c14n#"/><ds:SignatureMethod Algorithm="http://www.w3.org/2001/04/xmldsig-more#gostr34102001-gostr3411"/><ds:Reference URI="#SIGNED_BY_CALLER"><ds:Transforms><ds:Transform Algorithm="http://www.w3.org/2001/10/xml-exc-c14n#"/><ds:Transform Algorithm="urn://smev-gov-ru/xmldsig/transform"/></ds:Transforms><ds:DigestMethod Algorithm="http://www.w3.org/2001/04/xmldsig-more#gostr3411"/><ds:DigestValue>moG0idxAfz8FCbFeiYuc1au+nOx1n0nur54ICEovnsI=</ds:DigestValue></ds:Reference></ds:SignedInfo><ds:SignatureValue>oRhlceCP3ZT3H7jcKgooXNMFnfQhvUoLz3R4D/3TvB5RxnUtMLEssffjZHk34p5NWFTPLPpRCNm5EIiNTi3ulA==</ds:SignatureValue><ds:KeyInfo><ds:X509Data><ds:X509Certificate>MIIBjzCCAT6gAwIBAgIFAK0bIlkwCAYGKoUDAgIDMDExCzAJBgNVBAYTAlJVMRIwEAYDVQQKDAlDcnlwdG9Qcm8xDjAMBgNVBAMMBUFsaWFzMB4XDTE4MDkyNTEyMTgwMFoXDTE5MDkyNTEyMTgwMFowMTELMAkGA1UEBhMCUlUxEjAQBgNVBAoMCUNyeXB0b1BybzEOMAwGA1UEAwwFQWxpYXMwYzAcBgYqhQMCAhMwEgYHKoUDAgIkAAYHKoUDAgIeAQNDAARA1/RkKouLLrgR33bZYmaJslhiYtsEuaEcn4VV/w8f8nI7RZpIkKt+AIOYiIrmP1/DSjvmSgw17Jwt/oI3DdGvhaM7MDkwDgYDVR0PAQH/BAQDAgPoMBMGA1UdJQQMMAoGCCsGAQUFBwMCMBIGA1UdEwEB/wQIMAYBAf8CAQUwCAYGKoUDAgIDA0EA81lwsJ/jkOSXBp06HYDQL95pBNgrWDaODEq6sdnB8CFPg0VoDbNzI1m/YGaTdBpz8IvYJUjXIYv+28Kw+7Py1w==</ds:X509Certificate></ds:X509Data></ds:KeyInfo></ds:Signature></ns:CallerInformationSystemSignature></ns:AckRequest></soapenv:Body></soapenv:Envelope>"""

# Версия 1.2
form_data = {
    "type": "checkxml",
    "schemaVersion": "20",
    "textarea-area": xml_text,
}

rs = requests.post("https://smev3.gosuslugi.ru/portal/checkxmlform", data=form_data)
print(rs.json())

# Версия 1.1
form_data["schemaVersion"] = "10"

rs = requests.post("https://smev3.gosuslugi.ru/portal/checkxmlform", data=form_data)
print(rs.json())
