#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# Example:
#     case "{OPERATION}": {
#         Crypto::CryptoWsdl:{OPERATION}Document doc = Crypto::CryptoWsdl:{OPERATION}Document.Factory.newInstance();
#         doc.ensure{OPERATION}().ensure{OPERATION}Rq();
#         return doc;
#     }
TEMPLATE_CASE = """\
<xsc:Item><xsc:Java>
    case "{OPERATION}": {
        </xsc:Java>
                    </xsc:Item>
                    <xsc:Item>
                      <xsc:TypeDeclaration TypeId="451" Path="xsdQE2W4SV3SHNRDDXBABIFNQAAAE" extStr="{OPERATION}Document">
                        <xsc:Presentation>Crypto::CryptoWsdl:{OPERATION}Document</xsc:Presentation>
                      </xsc:TypeDeclaration>
                    </xsc:Item>
                    <xsc:Item>
                      <xsc:Java> doc = </xsc:Java>
                    </xsc:Item>
                    <xsc:Item>
                      <xsc:TypeDeclaration TypeId="451" Path="xsdQE2W4SV3SHNRDDXBABIFNQAAAE" extStr="{OPERATION}Document">
                        <xsc:Presentation>Crypto::CryptoWsdl:{OPERATION}Document</xsc:Presentation>
                      </xsc:TypeDeclaration>
                    </xsc:Item>
                    <xsc:Item>
                      <xsc:Java>.Factory.newInstance();
        doc.ensure{OPERATION}().ensure{OPERATION}Rq();
        return doc;
    }
</xsc:Java></xsc:Item>
"""

# Example:
#     switch (operationName) {
#         {SWITCHES}
#
#         default: {
#             String text = String.format("Operation \"%s\" is not yet supported", operationName);
#             Radix::Explorer.Utils::Trace.warning(getEnvironment(), text);
#             throw new UnsupportedOperationException(text);
#         }
#     }
TEMPLATE = """
                  <Src>
                    <xsc:Item>
                      <xsc:Java>switch (operationName) {</xsc:Java></xsc:Item>
{SWITCHES}
    <xsc:Item><xsc:Java>
    default: {
        String text = String.format(</xsc:Java>
                    </xsc:Item>
                    <xsc:Item>
                      <xsc:LocalizedString StringId="mls3QUBDE5HFVFYTBPB2TMRTFX42Y"/>
                    </xsc:Item>
                    <xsc:Item>
                      <xsc:Java>, operationName);
        </xsc:Java>
                    </xsc:Item>
                    <xsc:Item>
                      <xsc:TypeDeclaration TypeId="411" Path="apcSC2X2DZATHORDGZJABIFNQAABA">
                        <xsc:Presentation>Radix::Explorer.Utils::Trace</xsc:Presentation>
                      </xsc:TypeDeclaration>
                    </xsc:Item>
                    <xsc:Item>
                      <xsc:Java>.</xsc:Java>
                    </xsc:Item>
                    <xsc:Item>
                      <xsc:IdReference Path="apcSC2X2DZATHORDGZJABIFNQAABA mth7NHMFKQRS5B7HI3ABYPBZBNVPQ" Invoke="true">
                        <xsc:Presentation>warning</xsc:Presentation>
                      </xsc:IdReference>
                    </xsc:Item>
                    <xsc:Item>
                      <xsc:Java>(getEnvironment(), text);
        throw new UnsupportedOperationException(text);
    }
}
</xsc:Java></xsc:Item>
                  </Src>
"""

ITEMS = [
    'CalcArpc', 'CalcArqc', 'CalcCsc', 'CalcCvv', 'CalcEmvMac', 'CalcHmac', 'CalcKeyCheck', 'CalcMac', 'CalcMacDukpt',
    'CalcPinOffset', 'CalcPvv', 'CheckArpc', 'CheckArqc', 'CheckCapToken', 'CheckCsc', 'CheckCvc3', 'CheckCvv',
    'CheckDcsc', 'CheckDcvv', 'CheckHmac', 'CheckKey', 'CheckMac', 'CheckMacDukpt', 'CheckPinOffset', 'CheckPvv',
    'CheckRsaKey', 'DecryptDukpt', 'DesCrypt', 'DesRecrypt', 'EncryptDukpt', 'ExportEmvPinBlock', 'ExportHmacKey',
    'ExportKey', 'ExportPinBlock', 'ExportRsaKey', 'GenHmacKey', 'GenKey', 'GenRsaKey', 'GeneratePin', 'GetHsmInfo',
    'ImportClearPin', 'ImportHmacKey', 'ImportKey', 'ImportPinBlock', 'ImportPinBlockDukpt', 'ImportPinOffset',
    'ImportRsaKey', 'JwtDecode', 'JwtEncode', 'MigrateKey', 'RebuildPinBlock', 'RklGenerateAndEncryptKey',
    'RklImportPublicKey', 'RklImportRootPublicKey', 'RsaSign', 'RsaVerify', 'TdsSign', 'TranslateKey'
]

cases = [
    TEMPLATE_CASE.replace('{OPERATION}', operation)
    for operation in ITEMS
]
text = TEMPLATE.replace('{SWITCHES}', '\n'.join(cases))

with open('switch_case.xml', 'w', encoding='utf-8') as f:
    print(text)
    print(text, file=f)
