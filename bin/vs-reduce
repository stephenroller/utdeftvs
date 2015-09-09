#!/usr/bin/env python2.7

import sys
import argparse
from collections import defaultdict
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

def memory_grouper(keyvalstream):
    memory = {}
    for key, val in keyvalstream:
        memory[key] = memory.get(key, 0) + val
    return ((k, [(k, v)]) for k, v in memory.iteritems())

def memory_grouper_sort(keyvalstream):
    memory = defaultdict(int)
    for key, val in keyvalstream:
        memory[key] += val
    keys = memory.keys()
    keys.sort()
    return ((k, [(k, memory[k])]) for k in keys)

def memory_grouper_sort_val(keyvalstream):
    memory = defaultdict(int)
    for key, val in keyvalstream:
        memory[key] += val
    keys = memory.keys()
    keys.sort(key=lambda x: -memory[x])
    return ((k, [(k, memory[k])]) for k in keys)



def main():
    parser = argparse.ArgumentParser(
        'Sums items with the same key. The items must be sorted with by the key, and the summed value must be the last column.')
    parser.add_argument('--input', '-i', metavar='[FILE|-]', help='Input vector space', type=argparse.FileType('r'), default=sys.stdin)
    parser.add_argument('--memory', action='store_true', help='Tally up the counts in memory. May cause memory issues.')
    parser.add_argument('--sort', action='store_true', help='Produce output sorted by key. May be very slow.')
    parser.add_argument('--sortval', action='store_true', help='Produce output sorted by key. May be very slow.')
    args = parser.parse_args()


    if args.memory:
        if args.sort:
            grouped = memory_grouper_sort(lines_to_keyval(args.input))
        elif args.sortval:
            grouped = memory_grouper_sort_val(lines_to_keyval(args.input))
        else:
            grouped = memory_grouper(lines_to_keyval(args.input))
    else:
        grouped = groupby(lines_to_keyval(args.input), key=lambda x: x[0])

    # group items with the same key
    for key, group in grouped:
        # sum up all their values
        vs = sum(v for k, v in group)
        # and output the summed pair
        if int(vs) == vs:
            vs = int(vs)
        if isinstance(vs, int):
            print "%s\t%d" % (key, vs)
        else:
            print "%s\t%f" % (key, vs)

if __name__ == '__main__':
    main()

