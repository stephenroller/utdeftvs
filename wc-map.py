#!/usr/bin/env python2.7

import sys
import argparse
from collections import Counter
from util import pos, bigrams

def main():
    parser = argparse.ArgumentParser(description='Wordcount mapper')
    parser.add_argument('--input', '-i', metavar='[FILE|-]', help='Input vector space', type=argparse.FileType('r'), default=sys.stdin)
    args = parser.parse_args()

    wc = Counter()
    for line in args.input:
        line = line.strip().split(" ")
        wc.update(line)

    for k, v in wc.iteritems():
        print "%s\t%d" % (k, v)


if __name__ == '__main__':
    main()

