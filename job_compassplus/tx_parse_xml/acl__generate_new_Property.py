#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import re
import uuid

from pathlib import Path

from bs4 import BeautifulSoup


FILE_NAME_ACL = Path(
    r"C:\DEV__TX\trunk_tx\com.tranzaxis\ads\Interfacing.W4\src\aclTJQ2GCOP7NFZPERU23FQA76GXQ.xml"
)
FILE_NAME_ACL_LOCALE = (
    FILE_NAME_ACL.parent.parent / "locale" / "en" / ("mlb" + FILE_NAME_ACL.name)
)

root_acl = BeautifulSoup(open(FILE_NAME_ACL, "rb"), "xml")
root_acl_locale = BeautifulSoup(open(FILE_NAME_ACL_LOCALE, "rb"), "xml")

# NOTE: <Group Id="cpg<...>" Name="<...>" Members="<PROP_IDS">
PROP_IDS = "prd45TLQNSG4ZHKBNA47FXMPPU2DA prdSMVLMMHGBNFZDPKTLREQIMZQQI prdO2NOBXHOF5GQ7GZNU72X7AHINA prdUCW5JGR3ERH57BHQZW6A5ICD3Y prdOBM2S7OY3NEGNKNH2ICNFYBBJM prd44YUSXQGX5EWRDH5KNLZW3HQY4 prdK6OZ5JDUPFHDFEOYPUV743YE4Q prdZBIQDTOORBBJ5LCGRJIZUTOR2M prdPIVNTR5EERAHLGOWNB2H3OM674 prdZ77U22XJOZA75HI3VOPQMRGEMQ prd7HEZYF7WEBE33BTYCW5JZBR7TM prdKDRVNDR2WZHDZNAWVUFTNQDMXM prdWW4PDFFYP5DHVNGYY5PFUDZKSU prdH273DPBJCJH5RIO7XOEDA264K4 prdLOZ3LGQ6O5DCJMCJKCDCNHCDTY prdXIJRCNSMUVB5NM7XWSEKNIB7VM prdM3TWEJNXGZHJPF2RYCSOVO5DCY prdU2ZTHQSTMFGSHHDZMAN4HHVEQY prd67BZTCTYZ5B5VJ2XHTEMF4GPTU prdU4ZPUTPJOVEAXB2STEOR75N4PM prdOSEMPZYRR5HMVG7QPW6HQJJUNQ prdE3XVETDHQVAG7F4AI2XMHTTNAE prdDSS3XKFQ7VFV3FTNVY72ZPFXNI prdMVSBYDI2MZA2ZJN7E5NIYKFOS4 prd3YGIB5LSA5CY5L6Z5SPX2IDHNU prdVBGG254XNNDFXIKVTOGGGC7RCE prdFJWE4R7BFRC7JDREKN45LKJE6Y prdDLGUFA7MFJEOXK2TDN5NEXK6JY prdJII6QJNJVFHZ5NWE6NPJJYJNAY prdMJQG63HJ4JAZ5KWGNUJASMEE6M prdDEIUSASLFJDV3P7FEEBJ3JC4IY prdIFMA4QRICFDD3GVNV4ERFEXIKQ prdGK3RLNHSJVD5DBZOU4MF3IZQHU prdDKTJ7TT7W5G4RGOLSQGRXDSDIA prd5CVKNF4PPNGAJDAWKIOJRSGGL4".split()
items = []

new_prop_ids = []

with open("new_props.txt", "w", encoding="utf-8") as f:
    for prop_id in PROP_IDS:
        prop_el = root_acl.select_one(f'[Id="{prop_id}"]')
        prop_name = prop_el["Name"]

        title_id = prop_el.Presentation["TitleId"]
        title = root_acl_locale.select_one(f'[Id="{title_id}"]').Value.text

        # print(name, title)
        prop_el["Id"] = f"prd{uuid.uuid4().hex.upper()[:26]}"
        prop_el["Name"] = f"{prop_name}_Title_{title}"

        new_prop_ids.append(prop_el["Id"])

        new_src = f"""\
            <Src>
                <xsc:Item>
                    <xsc:Java>return </xsc:Java>
                </xsc:Item>
                <xsc:Item>
                    <xsc:IdReference Path="{FILE_NAME_ACL.stem} {prop_id}" Invoke="true">
                        <xsc:Presentation>{prop_name}</xsc:Presentation>
                    </xsc:IdReference>
                </xsc:Item>
                <xsc:Item>
                    <xsc:Java>;</xsc:Java>
                </xsc:Item>
            </Src>\
        """

        new_prop_el_str = re.sub(
            "<Src>.+?</Src>", new_src, str(prop_el), flags=re.DOTALL
        )
        print(new_prop_el_str, file=f)

    f.write("\n\n")
    f.write('new_prop_ids: "' + " ".join(new_prop_ids) + '"')
