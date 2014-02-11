#!/usr/bin/env python

import sys
from collections import namedtuple

fieldnames = "word lemma pos id att rela".split()
nodetuple = namedtuple('PieceTuple', fieldnames)

class Node(object):
    def __init__(self, word, lemma, pos, wid, watt, rela):
        self.word = word
        self.lemma = lemma
        self.pos = pos
        self.id = wid
        self.watt = watt
        self.rela = rela
        self.parent = None
        self.children = []

    def __repr__(self):
        return "[%s/%s/%s %s]" % (self.word, self.pos, self.rela, ", ".join(repr(c) for c in self.children))

f = open("bnc.parsed.txt")

for lineno, line in enumerate(f):
    line = line.rstrip("\n")
    if lineno > 1000:
        break
    if line.startswith("<text"):
        continue
    elif line == "</text>":
        continue
    else:
        fields = line.split("\t")
        assert len(fields) % 6 == 0
        rootnode = Node('RT', 'RT', 'RT', '0', '0', '')
        words = {'0': rootnode}
        while fields:
            chunk, fields = fields[:6], fields[6:]
            n = Node(*chunk)
            words[n.id] = n
        for n in words.itervalues():
            if n is not rootnode:
                n.parent = words[n.watt]
                n.parent.children.append(n)

        print repr(rootnode)


