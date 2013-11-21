#!/usr/bin/env python2.7

"""
Converts from DHG's TLP (Text, Lemma, POS) format into CoNLL format
for use as input to the MaltParser.

TLP format is one sentence per line,

TEXTID <tab> TYPE <tab> SENTENCE1 <tab> SENTENCE2 <tab> ...
SENTENCE := WORD1 <space> WORD2 <space> ...
WORD := TOKEN '|' LEMMA '|' POS

"""

import sys

def fix_pos(pos, lemma):
    direct_fixes = {
        '-LRB-' : '(',
        '-RRB-' : ')',
        '-LSB-' : '(',
        '-RSB-' : ')',
        '-LCB-' : '(',
        '-RCB-' : ')',
        '.' : 'SENT',
        'NNPS' : 'NPS',
        'NNP' : 'NP',
        'PRP' : 'PP',
        'PRP$' : 'PP$',

    }
    if pos in direct_fixes:
        return direct_fixes[pos]
    pos2 = pos[:2]
    # handle the verbs be and have
    if lemma == 'have' and pos2 == 'VB':
        return pos[0] + 'H' + pos[2:]
    elif lemma == 'be' and pos2 == 'VB':
        return pos
    elif pos2 == 'VB':
        return pos[0] + 'V' + pos[2:]
    else:
        # unchanged
        return pos

def main():
    for docno, line in enumerate(sys.stdin, 1):
        line = line.strip()
        split = line.split("\t")
        key = split[0]
        sentences = split[2:]
        for s in sentences:
            words = s.split(" ")
            tlps = (w.split("|") for w in words)
            lemmapos = (w[1] + "/" + fix_pos(w[2], w[1]) for w in tlps)
            print " ".join(lemmapos)


if __name__ == '__main__':
    main()

