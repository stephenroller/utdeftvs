#!/usr/bin/env python2.7

import sys
import argparse
from collections import Counter
from util import pos, bigrams

def main():
    parser = argparse.ArgumentParser(description='Wordcount mapper')
    parser.add_argument('--input', '-i', metavar='[FILE|-]', help='Input vector space', type=argparse.FileType('r'), default=sys.stdin)
    parser.add_argument('--adjnoun', action='store_true', help='Compute counts for adj-nouns.')
    parser.add_argument('--nounnoun', action='store_true', help='Compute counts for noun-nouns.')
    args = parser.parse_args()

    wc = Counter()
    for line in args.input:
        line = line.strip().split(" ")
        if args.adjnoun:
            # adjnoun bigram count
            adjnouns = ("%s__%s" % (l, r) for i, (l, r) in bigrams(line) if pos(l) == "a" and pos(r) == "n")
            wc.update(adjnouns)
        elif args.nounnoun:
            # nounnoun bigram count
            nounnouns = ("%s__%s" % (l, r) for i, (l, r) in bigrams(line) if pos(l) == "n" and pos(r) == "n")
            wc.update(nounnouns)
        else:
            # regular count
            wc.update(line)

    for k, v in wc.iteritems():
        print "%s\t%d" % (k, v)


if __name__ == '__main__':
    main()

