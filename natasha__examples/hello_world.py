#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


# SOURCE: https://github.com/natasha/natasha


# pip install natasha
from natasha import Segmenter, NewsEmbedding, NewsMorphTagger, Doc


tt = 'Появление ООН было обусловлено целым рядом объективных факторов'

segmenter = Segmenter()

emb = NewsEmbedding()
morph_tagger = NewsMorphTagger(emb)
doc = Doc(tt)
doc.segment(segmenter)
doc.tag_morph(morph_tagger)

for token in doc.tokens:
    print(f'[{token.start}:{token.stop}] {token.pos} {token.text!r}\n{token}\n')

"""
[0:9] NOUN 'Появление'
DocToken(stop=9, text='Появление', pos='NOUN', feats=<Inan,Nom,Neut,Sing>)

[10:13] PROPN 'ООН'
DocToken(start=10, stop=13, text='ООН', pos='PROPN', feats=<Inan,Gen,Fem,Sing>)

[14:18] AUX 'было'
DocToken(start=14, stop=18, text='было', pos='AUX', feats=<Imp,Neut,Ind,Sing,Past,Fin,Act>)

[19:30] VERB 'обусловлено'
DocToken(start=19, stop=30, text='обусловлено', pos='VERB', feats=<Perf,Neut,Sing,Past,Short,Part,Pass>)

[31:36] ADJ 'целым'
DocToken(start=31, stop=36, text='целым', pos='ADJ', feats=<Ins,Pos,Masc,Sing>)

[37:42] NOUN 'рядом'
DocToken(start=37, stop=42, text='рядом', pos='NOUN', feats=<Inan,Ins,Masc,Sing>)

[43:54] ADJ 'объективных'
DocToken(start=43, stop=54, text='объективных', pos='ADJ', feats=<Gen,Pos,Plur>)

[55:63] NOUN 'факторов'
DocToken(start=55, stop=63, text='факторов', pos='NOUN', feats=<Inan,Gen,Masc,Plur>)
"""
