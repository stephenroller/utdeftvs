#!/usr/bin/env python

import sys
import argparse

_FIELDNAMES = "word lemma pos id pid rel".split()

def sentenceExtractor(lineIterator):
    sentNo = 0
    title = ""
    buffer = []
    for line in lineIterator:
        line = line.strip()
        if line == "<s>":
            buffer = []
            sentNo += 1
        elif line == "</s>":
            yield "%s:%d" % (title, sentNo), buffer
        elif line.startswith("<text id=\""):
            title = line[10:-2]
            sentNo = 0
        elif line == "</text>":
            pass
        else:
            buffer.append(dict(zip(_FIELDNAMES, line.split())))

def outputLemmas(tupleIterator, usePos=True):
    if usePos:
        return ("%s/%s" % (t['lemma'], t['pos']) for t in tupleIterator)
    else:
        return (t['lemma'] for t in tupleIterator)

def main():
    parser = argparse.ArgumentParser(
                description='Extracts sentences or documents from minipar output.')
    parser.add_argument('--input', '-i', metavar='[FILE|-]', help='Input file')
    parser.add_argument('--nopos', '-P', action='store_false', help='Ignore POS tags.')
    args = parser.parse_args()

    if not args.input or args.input == "-":
        args.input = sys.stdin
    else:
        args.input = open(args.input)

    lines = sentenceExtractor(args.input)

    for lid, line in lines:
        linestr = " ".join(outputLemmas(line, usePos=args.nopos))
        #print "%s\t%s" % (lid, linestr)
        print linestr

    args.input.close()



if __name__ == '__main__':
    main()

