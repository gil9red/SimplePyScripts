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

for i, (error_indication, error_status, error_index, var_binds) in enumerate(items, 1):
    if error_indication:
        print(f'Error indication: {error_indication}')

    elif error_status:
        at = '?'
        if error_index:
            at = var_binds[int(error_index) - 1][0]
        print(f'Error status {error_status.prettyPrint()!r} at {at}')

    else:
        for var_bind in var_binds:
            var, value = var_bind
            print(var_bind)
            print(f'{var} = {value}')
            print(f'{var.getOid()} = {value}')
            print(f'{var.prettyPrint()} = {value.prettyPrint()}')
            print()
