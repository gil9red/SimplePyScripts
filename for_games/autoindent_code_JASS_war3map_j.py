#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


import re


DEBUG = False


def merge_str_literal(text: str) -> str:
    def _on_match(m: re.Match):
        return m.group().replace('"+"', "")

    return re.sub(r'".+?"(\+".+?")+ ', _on_match, text)


lines = """
function II1I1_II takes real II1I1__I returns nothing
local real II1I1_1I
local real st=TimerGetElapsed(II1I___I)
if st<=0 then
set II1I___I=CreateTimer()
call TimerStart(II1I___I,1000000,false,null)
endif
if(II1I1__I>0)then
loop
set II1I1_1I=II1I1__I-TimerGetElapsed(II1I___I)+st
exitwhen II1I1_1I<=0
if(II1I1_1I>bj_POLLED_WAIT_SKIP_THRESHOLD)then
call TriggerSleepAction(0.1*II1I1_1I)
else
call TriggerSleepAction(bj_POLLED_WAIT_INTERVAL)
endif
endloop
endif
endfunction
""".strip().splitlines()

stack = []
items = []
for line in lines:
    if line.startswith("globals"):
        stack.append("globals")

    elif line.startswith("endglobals"):
        stack.pop(-1)
        stack.append("endglobals")

    elif line.startswith("function"):
        stack.append("function")

    elif line.startswith("endfunction"):
        stack.pop(-1)
        stack.append("endfunction")

    elif line.startswith("loop"):
        stack.append("loop")

    elif line.startswith("endloop"):
        stack.pop(-1)
        stack.append("endloop")

    elif line.startswith("if"):
        stack.append("if")

    elif line.startswith("elseif"):
        stack.pop(-1)
        stack.append("elseif")

    elif line.startswith("else"):
        stack.pop(-1)
        stack.append("else")

    elif line.startswith("endif"):
        stack.pop(-1)
        stack.append("endif")
    else:
        stack.append(line[:8] + "...")

    indent = len(stack) - 1
    line = merge_str_literal(line)
    items.append("    " * indent + line)

    DEBUG and print(f"{indent}. {line!r}", stack)

    # Add empty line after endglobals and endfunction
    if line.startswith("endglobals") or line.startswith("endfunction"):
        items.append("")

    if stack[-1] not in ["globals", "function", "loop", "if", "elseif", "else"]:
        stack.pop(-1)


new_text = "\n".join(items).strip()
print(new_text)
"""
function II1I1_II takes real II1I1__I returns nothing
    local real II1I1_1I
    local real st=TimerGetElapsed(II1I___I)
    if st<=0 then
        set II1I___I=CreateTimer()
        call TimerStart(II1I___I,1000000,false,null)
    endif
    if(II1I1__I>0)then
        loop
            set II1I1_1I=II1I1__I-TimerGetElapsed(II1I___I)+st
            exitwhen II1I1_1I<=0
            if(II1I1_1I>bj_POLLED_WAIT_SKIP_THRESHOLD)then
                call TriggerSleepAction(0.1*II1I1_1I)
            else
                call TriggerSleepAction(bj_POLLED_WAIT_INTERVAL)
            endif
        endloop
    endif
endfunction
"""
