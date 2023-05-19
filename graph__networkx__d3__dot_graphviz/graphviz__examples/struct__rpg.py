#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


# pip install graphviz
from graphviz import Digraph


g = Digraph("rpg", filename="test-output/rpg.gv", node_attr={"shape": "plaintext"})

g.node(
    "equipment",
    """<
<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0">
  <TR>
    <TD PORT="id_1">sword</TD>
    <TD PORT="id_2">shield</TD>
    <TD PORT="id_3">ax</TD>
  </TR>
  <TR>
    <TD PORT="id_4">helmet</TD>
    <TD PORT="id_5">chain mail</TD>
    <TD PORT="id_6"></TD>
  </TR>
</TABLE>>""",
)

g.node(
    "person",
    """<
<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="4">
  <TR>
    <TD></TD>
    <TD PORT="head">HEAD</TD>
    <TD></TD>
  </TR>
  <TR>
    <TD PORT="right">RIGHT</TD>
    <TD PORT="body">BODY</TD>
    <TD PORT="left">LEFT</TD>
  </TR>
  <TR>
    <TD></TD>
    <TD PORT="legs">LEGS</TD>
    <TD></TD>
  </TR>
</TABLE>>""",
)

g.edge("person:head", "equipment:id_4")
g.edge("person:right", "equipment:id_1")
g.edge("person:left", "equipment:id_3")
g.edge("person:body", "equipment:id_5")

g.view()
