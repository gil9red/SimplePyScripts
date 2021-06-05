#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# SOURCE: http://www.oidview.com/mibs/0/SNMPv2-MIB.html


from typing import Iterator

# pip install pysnmp
from pysnmp.hlapi import nextCmd, SnmpEngine, CommunityData, UdpTransportTarget, ContextData, ObjectType, ObjectIdentity


def get_iterator(host: str, port: int = 161, community: str = '') -> Iterator:
    hrProcessorLoad = '1.3.6.1.2.1.25.3.3.1.2'

    return nextCmd(
        SnmpEngine(),
        CommunityData(community, mpModel=0),
        UdpTransportTarget((host, port)),
        ContextData(),
        ObjectType(ObjectIdentity(hrProcessorLoad)),
        lexicographicMode=False,
    )


iterator = get_iterator('localhost', 161, 'public')
items = list(iterator)
print(f"Number CPU cores: {len(items)}\n")

for i, (errorIndication, errorStatus, errorIndex, varBinds) in enumerate(items, 1):
    if errorIndication:
        print(f'Error indication: {errorIndication}')

    elif errorStatus:
        print(f'Error status {errorStatus.prettyPrint()!r} at {errorIndex and varBinds[int(errorIndex) - 1][0] or "?"}')

    else:
        for varBind in varBinds:
            var, value = varBind
            print(f'CPU Core #{i}')
            print(varBind)
            print(f'{var} = {value}')
            print(f'{var.prettyPrint()} = {value.prettyPrint()}')
            print()
