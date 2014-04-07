#!/usr/bin/env python2.7

"""
Converts from DHG's TLP (Text, Lemma, POS) format into CoNLL format
for use as input to the MaltParser.

TLP format is one document per line,

TEXTID <tab> TYPE <tab> SENTENCE1 <tab> SENTENCE2 <tab> ...
SENTENCE := WORD1 <space> WORD2 <space> ...
WORD := TOKEN '|' LEMMA '|' POS

"""

import sys
import argparse
import itertools

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
    parser = argparse.ArgumentParser(
                description="Extracts text from Dan's TLP format.")
    parser.add_argument('--input', '-i', metavar='[FILE|-]', type=argparse.FileType('r'), help='Input file', default=sys.stdin)
    parser.add_argument('--doclines', '-d', action='store_true', help='Output one document per line.')
    parser.add_argument('--pos', '-p', action='store_true', help='Output with POS tags.')
    parser.add_argument('--lemmas', '-l', action='store_true', help='Output lemmas instead of surface forms.')
    args = parser.parse_args()

    for docno, line in enumerate(sys.stdin, 1):
        line = line.strip()
        split = line.split("\t")
        #key = split[0]
        sentences = split[2:]
        if args.doclines:
            sentences = [" ".join(sentences)]
        for s in sentences:
            words = s.split(" ")
            tlps = (w.split("|") for w in words)
            tlps = (w for w in tlps if len(w) == 3)
            tlps = ((w[0], w[1], fix_pos(w[2], w[1])) for w in tlps)
            indx = args.lemmas and 1 or 0
            if args.pos:
                output = (w[indx] + "/" + w[2] for w in tlps)
            else:
                output = (w[indx] for w in tlps)
            print " ".join(output).strip()


if __name__ == '__main__':
    main()

