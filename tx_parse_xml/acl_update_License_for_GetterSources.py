#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from pathlib import Path
import re

from bs4 import BeautifulSoup


FILE_NAME_ACL = Path(r'C:\<...>\ads\<...>\src\<...>.xml')
LICENSE_PATH = "<...>/<...>/<...>/"

TEMPLATE_THIS_PROP = """
    <xsc:Item>
      <xsc:IdReference Path="{acl_id} {prop_id}" Invoke="true" extStr="#STD_PROP_VALUE#">
        <xsc:Presentation>{prop_name}</xsc:Presentation>
      </xsc:IdReference>
    </xsc:Item>
"""
TEMPLATE = """
        <GetterSources>
          <Src>
            <xsc:Item>
              <xsc:Java>if (</xsc:Java>
            </xsc:Item>
            {TEMPLATE_THIS_PROP}
            <xsc:Item>
              <xsc:Java> == null) {
    try {
        </xsc:Java>
            </xsc:Item>
            <xsc:Item>
              <xsc:ReadLicense Id="1" License="{license_path}{license_name}"/>
            </xsc:Item>
            <xsc:Item>
              <xsc:Java>
        </xsc:Java>
            </xsc:Item>
            <xsc:Item>
              <xsc:CheckLicense Id="1" License="{license_path}{license_name}"/>
            </xsc:Item>
            <xsc:Item>
              <xsc:Java>
        
        </xsc:Java>
            </xsc:Item>
            {TEMPLATE_THIS_PROP}
            <xsc:Item>
              <xsc:Java> = true;
        
    } catch (java.lang.Exception e) {
        </xsc:Java>
            </xsc:Item>
            <xsc:Item>
              <xsc:IdReference Path="{acl_id} mth7M2ITEYXHBAVRLUEALT3VHXFAQ" Invoke="true">
                <xsc:Presentation>handleErrorWithCheckLicense</xsc:Presentation>
              </xsc:IdReference>
            </xsc:Item>
            <xsc:Item>
              <xsc:Java>(e);
        </xsc:Java>
            </xsc:Item>
            {TEMPLATE_THIS_PROP}
            <xsc:Item>
              <xsc:Java> = false;
    }
}

return </xsc:Java>
            </xsc:Item>
            {TEMPLATE_THIS_PROP}
            <xsc:Item>
              <xsc:Java>;
</xsc:Java>
            </xsc:Item>
          </Src>
        </GetterSources>
"""

ITEMS = [
    ...
]

root_acl = BeautifulSoup(open(FILE_NAME_ACL, 'rb'), 'xml')
root_acl_str = str(root_acl)

for license_name, license_id, prop_name, prop_id in ITEMS:
    print(license_name, license_id, prop_name, prop_id)

    new_getter_src = TEMPLATE \
        .replace('{TEMPLATE_THIS_PROP}', TEMPLATE_THIS_PROP) \
        .replace('{prop_id}', prop_id) \
        .replace('{prop_name}', prop_name) \
        .replace('{license_path}', LICENSE_PATH) \
        .replace('{license_name}', license_id) \
        .replace('{acl_id}', FILE_NAME_ACL.stem)

    prop_el = root_acl.select_one(f'[Id="{prop_id}"]')
    old_prop_el_str = str(prop_el)
    new_prop_el_str = re.sub('<GetterSources>.+?</GetterSources>', new_getter_src, old_prop_el_str, flags=re.DOTALL)
    root_acl_str = root_acl_str.replace(old_prop_el_str, new_prop_el_str)

with open('new_' + FILE_NAME_ACL.name, 'w', encoding='utf-8') as f:
    f.write(root_acl_str)
