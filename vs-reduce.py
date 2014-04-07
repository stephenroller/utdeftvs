#!/usr/bin/env python2.7

import sys
import argparse
from itertools import groupby

def lines_to_keyval(stream):
    for line in stream:
        # split on tabs
        line = line.strip().split("\t")
        # value is the last item, key is the other columns
        key, val = line[:-1], line[-1]
        key = "\t".join(key)
        try:
            # prefer ints
            val = int(val)
        except:
            # but fall back to floats
            val = float(val)
        yield (key, val)

def main():
    parser = argparse.ArgumentParser(
        'Sums items with the same key. The items must be sorted with by the key, and the summed value must be the last column.')
    parser.add_argument('--input', '-i', metavar='[FILE|-]', help='Input vector space', type=argparse.FileType('r'), default=sys.stdin)
    args = parser.parse_args()


    # group items with the same key
    for key, group in groupby(lines_to_keyval(args.input), key=lambda x: x[0]):
        # sum up all their values
        vs = sum(v for k, v in group)
        # and output the summed pair
        if isinstance(vs, int):
            print "%s\t%d" % (key, vs)
        else:
            print "%s\t%f" % (key, vs)

if __name__ == '__main__':
    main()

