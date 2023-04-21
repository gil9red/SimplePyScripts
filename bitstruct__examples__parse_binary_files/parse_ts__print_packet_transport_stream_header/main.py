#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# SOURCE: https://en.wikipedia.org/wiki/MPEG_transport_stream#Packet

# https://github.com/eerimoq/bitstruct
# https://bitstruct.readthedocs.io/en/latest/

# pip install bitstruct
import bitstruct

import io


# SOURCE: https://nypromo2019.hb.bizmrg.com/video/man/ny2019__000.ts
#         from m3u8 https://github.com/gil9red/SimplePyScripts/blob/ad33a95c3f0487555e9d8a0a0c5aef00613c9bbf/html_parsing/https_newyear_mail_ru/download__m3u8.py
with open("ny2019__000.ts", "rb") as file:
    while True:
        data = file.read(188)
        if not data:
            break

        f = io.BytesIO(data)

        # 4-BYTE TRANSPORT STREAM HEADER
        print("4-BYTE TRANSPORT STREAM HEADER")
        sync_byte = f.read(1)
        print("sync_byte:", sync_byte)

        data = f.read(2)
        (
            transport_error_indicator,
            payload_unit_start_indicator,
            transport_priority,
            pid,
        ) = bitstruct.unpack(">b1b1b1u13", data)
        print("transport_error_indicator:", transport_error_indicator)
        print("payload_unit_start_indicator:", payload_unit_start_indicator)
        print("transport_priority:", transport_priority)
        print("pid:", pid)

        data = f.read(1)
        (
            transport_scrambling_control,
            adaptation_field_control,
            continuity_counter,
        ) = bitstruct.unpack(">u2u2u4", data)
        print("transport_scrambling_control:", transport_scrambling_control)
        print("adaptation_field_control:", adaptation_field_control)
        print("continuity_counter:", continuity_counter)
        print()

        # 184-BYTE <Adaptation field> + <Payload Data>
        # ...
