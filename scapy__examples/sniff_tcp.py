#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# https://github.com/secdev/scapy
# pip install scapy
from scapy.all import sniff


def _packethandler(pkt):
    data = pkt.summary()
    print(data)


sniff(filter="tcp", prn=_packethandler)
