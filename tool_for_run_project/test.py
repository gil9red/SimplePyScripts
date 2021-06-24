#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from go_v2 import (
    from_ghbdtn, SETTINGS, resolve_name, resolve_whats, resolve_version,
    get_similar_version_path, is_like_a_version
)


for k in SETTINGS:
    assert resolve_name(k) == k
    assert resolve_name(from_ghbdtn(k)) == k
assert resolve_name('t') == 'tx'
assert resolve_name('tx') == 'tx'
assert resolve_name('еч') == 'tx'
assert resolve_name('щзе') == 'optt'
assert resolve_name('o') == 'optt'
assert resolve_name('optt') == 'optt'


resolve_what = lambda alias: resolve_whats('tx', alias)[0]

for k in SETTINGS['tx']['whats']:
    assert resolve_what(k) == k
    assert resolve_what(from_ghbdtn(k)) == k
assert resolve_what('d') == 'designer'
assert resolve_what('в') == 'designer'
assert resolve_what('вуы') == 'designer'
assert resolve_what('e') == 'explorer'
assert resolve_what('b') == 'build'

assert resolve_version('tx', 'trunk') == 'trunk_tx'
assert resolve_version('еч', 'trunk') == 'trunk_tx'
assert resolve_version('optt', 'trunk') == 'trunk_optt'
assert resolve_version('щзе', 'trunk') == 'trunk_optt'

assert get_similar_version_path('tx', 'trunk')
assert get_similar_version_path('еч', 'trunk')

assert is_like_a_version('trunk')
assert is_like_a_version('3.2.22')
assert is_like_a_version('3.2.22.10')
