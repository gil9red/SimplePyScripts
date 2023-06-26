#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: http://www.oidview.com/mibs/0/SNMPv2-MIB.html


# pip install pysnmp
from pysnmp.hlapi import *


iterator = getCmd(
    SnmpEngine(),
    CommunityData("public", mpModel=0),
    UdpTransportTarget(("localhost", 161)),
    ContextData(),
    ObjectType(ObjectIdentity("SNMPv2-MIB", "sysDescr", 0)),
    ObjectType(ObjectIdentity("1.3.6.1.2.1.1.1.0")),  # OID, same as above
    ObjectType(ObjectIdentity(".1.3.6.1.2.1.1.1.0")),  # OID, same as above
)

error_indication, error_status, error_index, var_binds = next(iterator)

if error_indication:
    print(f"Error indication: {error_indication}")

elif error_status:
    at = "?"
    if error_index:
        at = var_binds[int(error_index) - 1][0]
    print(f"Error status {error_status.prettyPrint()!r} at {at}")

else:
    for var, value in var_binds:
        print(f"{var} = {value}")
        print(f"{var.getOid()} = {value}")
        print(f"{var.prettyPrint()} = {value.prettyPrint()}")
        print()
