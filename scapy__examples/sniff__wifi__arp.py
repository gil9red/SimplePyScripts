#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# SOURCE: http://www.secdev.org/projects/scapy/build_your_own_tools.html

# https://github.com/secdev/scapy
# pip install scapy
from scapy.all import *


"""
Here is another tool that will constantly monitor all interfaces on a machine and print all ARP request 
it sees, even on 802.11 frames from a Wi-Fi card in monitor mode. Note the store=0 parameter to sniff() 
to avoid storing all packets in memory for nothing. 
"""


def arp_monitor_callback(pkt):
    if ARP in pkt and pkt[ARP].op in (1, 2):  # who-has or is-at
        return pkt.sprintf("%ARP.hwsrc% %ARP.psrc%")


sniff(prn=arp_monitor_callback, filter="arp", store=0)
