#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# SOURCE: http://www.oidview.com/mibs/0/SNMPv2-MIB.html


# pip install pysnmp
from pysnmp.hlapi import *


iterator = getCmd(
    SnmpEngine(),
    CommunityData('public', mpModel=0),
    UdpTransportTarget(('localhost', 161)),
    ContextData(),
    ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysDescr', 0)),
    ObjectType(ObjectIdentity('1.3.6.1.2.1.1.1.0')),   # OID, same as above
    ObjectType(ObjectIdentity('.1.3.6.1.2.1.1.1.0')),  # OID, same as above
)

errorIndication, errorStatus, errorIndex, varBinds = next(iterator)

if errorIndication:
    print(f'Error indication: {errorIndication}')

elif errorStatus:
    print(f'Error status {errorStatus.prettyPrint()!r} at {errorIndex and varBinds[int(errorIndex) - 1][0] or "?"}')

else:
    for varBind in varBinds:
        var, value = varBind
        print(varBind)
        print(f'{var} = {value}')
        print(f'{var.prettyPrint()} = {value.prettyPrint()}')
        print()
