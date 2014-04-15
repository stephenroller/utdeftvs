#!/usr/bin/env python2.7

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

def outputLemmas(tupleIterator, usePos=True, useLemmas=True, lower=False):
    token_field = useLemmas and 'lemma' or 'word'
    if lower:
        lower_ = lambda x: x.lower()
    else:
        lower_ = lambda x: x

    if usePos:
        retval = ("%s/%s" % (lower_(t[token_field]), t['pos']) for t in tupleIterator)
    else:
        retval = (lower_(t[token_field]) for t in tupleIterator)

    return retval

def main():
    parser = argparse.ArgumentParser(
                description='Extracts sentences or documents from minipar output.')
    parser.add_argument('--input', '-i', metavar='[FILE|-]', help='Input file')
    parser.add_argument('--nopos', '-P', action='store_false', help='Ignore POS tags.')
    parser.add_argument('--nolemmatize', '-L', action='store_false', help="Don't lemmatize.")
    parser.add_argument('--forcelower', '-l', action='store_true', help='Force everything to be lowercase.')
    args = parser.parse_args()

    if not args.input or args.input == "-":
        args.input = sys.stdin
    else:
        args.input = open(args.input)

    lines = sentenceExtractor(args.input)

    for lid, line in lines:
        linestr = " ".join(outputLemmas(line, usePos=args.nopos, useLemmas=args.nolemmatize, lower=args.forcelower))
        #print "%s\t%s" % (lid, linestr)
        print linestr

    args.input.close()



if __name__ == '__main__':
    main()

