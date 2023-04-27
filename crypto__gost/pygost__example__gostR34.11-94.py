#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from pygost import gost341194
import base64


def get_digest(data, sbox=gost341194.DEFAULT_SBOX):
    if isinstance(data, str):
        data = data.encode("utf-8")

    gost_digest = gost341194.GOST341194(data, sbox)
    return (
        gost_digest.digest(),
        gost_digest.hexdigest(),
        base64.b64encode(gost_digest.digest()),
    )


text = """<soapenv:Body xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:wsu="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd" wsu:Id="body"><smev:GISGMPTransferMsg xmlns:smev="http://roskazna.ru/gisgmp/02000000/SmevGISGMPService/"><rev:Message xmlns:rev="http://smev.gosuslugi.ru/rev120315"><rev:Sender><rev:Code>RCPT00001</rev:Code><rev:Name>Отправитель</rev:Name></rev:Sender><rev:Recipient><rev:Code>MNSV10000</rev:Code><rev:Name>Государственная информационная система жилищно-коммунального хозяйства</rev:Name></rev:Recipient><rev:Originator><rev:Code>735111111</rev:Code><rev:Name>Получатель</rev:Name></rev:Originator><rev:ServiceName>GISGMP</rev:ServiceName><rev:TypeCode>GFNC</rev:TypeCode><rev:Status>REQUEST</rev:Status><rev:Date>2018-02-28T16:30:39.877+05:00</rev:Date><rev:ExchangeType>6</rev:ExchangeType></rev:Message><rev:MessageData xmlns:rev="http://smev.gosuslugi.ru/rev120315"><rev:AppData><gisgmp:RequestMessage xmlns:gisgmp="http://roskazna.ru/gisgmp/xsd/116/Message" Id="ID_4050460995" senderIdentifier="01309b2f-fdec-48cb-9de5-e7c52d6f7d04" senderRole="7" timestamp="2018-02-28T16:30:39.877+05:00"><msgd:ExportRequest xmlns:msgd="http://roskazna.ru/gisgmp/xsd/116/MessageData" kind="CHARGE"><pdr:Filter xmlns:pdr="http://roskazna.ru/gisgmp/xsd/116/PGU_DataRequest"><pdr:Conditions><pdr:ChargesIdentifiers><pdr:SupplierBillID>1234567890</pdr:SupplierBillID></pdr:ChargesIdentifiers></pdr:Conditions></pdr:Filter></msgd:ExportRequest></gisgmp:RequestMessage></rev:AppData></rev:MessageData></smev:GISGMPTransferMsg></soapenv:Body>"""
text = '<soapenv:Body xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:wsu="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd" wsu:Id="body"><smev:GISGMPTransferMsg xmlns:smev="http://roskazna.ru/gisgmp/02000000/SmevGISGMPService/"><rev:Message xmlns:rev="http://smev.gosuslugi.ru/rev120315"><rev:Sender><rev:Code>RCPT00001</rev:Code><rev:Name>Отправитель</rev:Name></rev:Sender><rev:Recipient><rev:Code>MNSV10000</rev:Code><rev:Name>Государственная информационная система жилищно-коммунального хозяйства</rev:Name></rev:Recipient><rev:Originator><rev:Code>735111111</rev:Code><rev:Name>Получатель</rev:Name></rev:Originator><rev:ServiceName>GISGMP</rev:ServiceName><rev:TypeCode>GFNC</rev:TypeCode><rev:Status>REQUEST</rev:Status><rev:Date>2018-02-28T16:30:39.877+05:00</rev:Date><rev:ExchangeType>6</rev:ExchangeType></rev:Message><rev:MessageData xmlns:rev="http://smev.gosuslugi.ru/rev120315"><rev:AppData><gisgmp:RequestMessage xmlns:gisgmp="http://roskazna.ru/gisgmp/xsd/116/Message" Id="ID_4050460995" senderIdentifier="01309b2f-fdec-48cb-9de5-e7c52d6f7d04" senderRole="7" timestamp="2018-02-28T16:30:39.877+05:00"><msgd:ExportRequest xmlns:msgd="http://roskazna.ru/gisgmp/xsd/116/MessageData" kind="CHARGE"><pdr:Filter xmlns:pdr="http://roskazna.ru/gisgmp/xsd/116/PGU_DataRequest"><pdr:Conditions><pdr:ChargesIdentifiers><pdr:SupplierBillID>1234567890</pdr:SupplierBillID></pdr:ChargesIdentifiers></pdr:Conditions></pdr:Filter></msgd:ExportRequest></gisgmp:RequestMessage></rev:AppData></rev:MessageData></smev:GISGMPTransferMsg></soapenv:Body>'

# print(get_digest(text)[2])
print(
    get_digest(text, "GostR3411_94_CryptoProParamSet")[2]
)
# /zP/7KpLyXyg6FpKsAjNNSMe3pvPjvfx24X9RdI9AYg=

# # text = """\
# # <soapenv:Envelope xmlns:rev="http://smev.gosuslugi.ru/rev120315" xmlns:smev="http://roskazna.ru/gisgmp/02000000/SmevGISGMPService/" xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:wsse="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd" xmlns:wsu="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd">
# # 	<soapenv:Header><wsse:Security soapenv:actor="http://smev.gosuslugi.ru/actors/smev"><wsse:BinarySecurityToken EncodingType="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-soap-message-security-1.0#Base64Binary" ValueType="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-x509-token-profile-1.0#X509v3" wsu:Id="CertId">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</wsse:BinarySecurityToken><ds:Signature xmlns:ds="http://www.w3.org/2000/09/xmldsig#"><ds:SignedInfo><ds:CanonicalizationMethod Algorithm="http://www.w3.org/2001/10/xml-exc-c14n#"></ds:CanonicalizationMethod><ds:SignatureMethod Algorithm="http://www.w3.org/2001/04/xmldsig-more#gostr34102001-gostr3411"></ds:SignatureMethod><ds:Reference URI="#body"><ds:Transforms><ds:Transform Algorithm="http://www.w3.org/2001/10/xml-exc-c14n#"></ds:Transform></ds:Transforms><ds:DigestMethod Algorithm="http://www.w3.org/2001/04/xmldsig-more#gostr3411"></ds:DigestMethod><ds:DigestValue>Lct/wB+HMMdVHYRc1+hu8WJvqXV9GtFO6E+xanFITUY=</ds:DigestValue></ds:Reference></ds:SignedInfo><ds:SignatureValue>fh3qrSzJ5Z018qO/hGpeD9E2NJJ2TuwqVFAJfA8qG7WFx6nHgar2q2nD7l3CNmb2kPsuyjPzO34assfQ2g2VLQ==</ds:SignatureValue><ds:KeyInfo><wsse:SecurityTokenReference><wsse:Reference URI="#CertId" ValueType="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-x509-token-profile-1.0#X509v3"></wsse:Reference></wsse:SecurityTokenReference></ds:KeyInfo></ds:Signature></wsse:Security></soapenv:Header><soapenv:Body wsu:Id="body">
# # 		<smev:GISGMPTransferMsg>
# # 			<rev:Message>
# # 				<rev:Sender>
# # 					<rev:Code>RKZN01001</rev:Code>
# # 					<rev:Name>Казначейство России</rev:Name>
# # 				</rev:Sender>
# # 				<rev:Recipient>
# # 					<rev:Code>RKZN01001</rev:Code>
# # 					<rev:Name>Казначейство России</rev:Name>
# # 				</rev:Recipient>
# # 				<rev:ServiceName>GISGMP</rev:ServiceName>
# # 				<rev:TypeCode>GFNC</rev:TypeCode>
# # 				<rev:Status>REQUEST</rev:Status>
# # 				<rev:Date>2017-09-12T09:30:47.0Z</rev:Date>
# # 				<rev:ExchangeType>6</rev:ExchangeType>
# # 				<rev:TestMsg>test</rev:TestMsg>
# # 			</rev:Message>
# # 			<rev:MessageData>
# # 				<rev:AppData>
# # 					<gisgmp:RequestMessage xmlns:com="http://roskazna.ru/gisgmp/xsd/116/Common" xmlns:ds="http://www.w3.org/2000/09/xmldsig#" xmlns:gisgmp="http://roskazna.ru/gisgmp/xsd/116/Message" xmlns:msgd="http://roskazna.ru/gisgmp/xsd/116/MessageData" xmlns:n1="http://www.altova.com/samplexml/other-namespace" xmlns:pdr="http://roskazna.ru/gisgmp/xsd/116/PGU_DataRequest" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" Id="ID_1" callBackURL="http://www.altova.com" senderIdentifier="1aaaaa" senderRole="1" timestamp="2017-09-12T09:30:47.0Z" xsi:schemaLocation="http://roskazna.ru/gisgmp/xsd/116/Message Message.xsd">
# # 						<msgd:ExportRequest Id="ID_2" kind="CHARGESTATUS">
# # 							<pdr:Filter>
# # 								<pdr:Conditions>
# # 									<pdr:ChargesIdentifiers>
# # 										<pdr:SupplierBillID>32187624486580332638</pdr:SupplierBillID>
# # 									</pdr:ChargesIdentifiers>
# # 								</pdr:Conditions>
# # 							</pdr:Filter>
# # 						</msgd:ExportRequest>
# # 					</gisgmp:RequestMessage>
# # 				</rev:AppData>
# # 			</rev:MessageData>
# # 		</smev:GISGMPTransferMsg>
# # 	</soapenv:Body>
# # </soapenv:Envelope>
# # """
#
# from io import StringIO, BytesIO
# import lxml.etree as et
# root = et.parse(StringIO(text))
# # print(et.tostring(root, encoding='utf-8').decode('utf-8'))
# # print()
#
# output = BytesIO()
# # root.write_c14n(output, exclusive=True)
# root.write_c14n(output, exclusive=True, with_comments=False)
# print(output.getvalue().decode('utf-8'))
#
# # # Lct/wB+HMMdVHYRc1+hu8WJvqXV9GtFO6E+xanFITUY=
# # print(get_digest(text, 'GostR3411_94_CryptoProParamSet')[2])
