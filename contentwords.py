#!/usr/bin/env python2.7

import sys
import argparse

GOOD_POS = dict(JJ="a", NN="n", NP="p", VV="v", RB="r")
GOOD_SHORT_POS = set(GOOD_POS.values())

def with_nice_pos(word_pos):
    if not word_pos:
        return False
    pos = word_pos.split("/")[-1]
    word = "".join(word_pos.split("/")[:-1])
    if '__' in word_pos or pos[:2] not in GOOD_POS:
        return (word, pos, pos)
    else:
        shortpos = GOOD_POS[pos[:2]]
        return (word, pos, shortpos)

def main():
    parser = argparse.ArgumentParser(
                description='Filters non-content words from a given vs corpus.')
    parser.add_argument('--input', '-i', metavar='[FILE|-]', type=argparse.FileType('r'), help='Input file', default=sys.stdin)
    parser.add_argument('--filterpos', '-p', action='store_true', help='Filter content words using the POS tags.')
    parser.add_argument('--shortpos', action='store_true', help='Output short POS tags.')
    parser.add_argument('--nopos', '-P', action='store_true', help="Don't output any POS tags.")
    parser.add_argument('--stopwords', '-s', metavar='FILE', type=argparse.FileType('r'), help='Stopwords file.')
    parser.add_argument('--dontlower', '-L', action='store_true', help="Don't lowercase words.")
    args = parser.parse_args()

    stopwords = set()
    if args.stopwords:
        stopwords = set(l.strip().split("\t")[0] for l in args.stopwords)

    inpt = args.input

    for sentence in inpt:
        sentence = sentence.strip().split(" ")
        sentence = (w for w in sentence if w)
        sentence = (with_nice_pos(wp) for wp in sentence)

        if args.filterpos:
            sentence = ((w, p, np) for w, p, np in sentence if np in GOOD_SHORT_POS)
        if stopwords:
            sentence = ((w, p, np) for w, p, np in sentence if w.lower() not in stopwords)
        if not args.dontlower:
            sentence = ((np == "p" and w or w.lower(), p, np) for w, p, np in sentence)

        if args.nopos:
            sentence = (w for w, p, np in sentence)
        elif args.shortpos:
            sentence = (w + "-" + np for w, p, np in sentence)
        else:
            sentence = (w + "/" + p for w, p, np in sentence)

        print " ".join(sentence)


if __name__ == '__main__':
    main()

